from twilio.rest import Client
from datetime import datetime
from hx711 import HX711
import RPi.GPIO as GPIO
import time

# Twilio API Parameters
TWILIO_ACCOUNT_SID = "<SID>"
TWILIO_AUTH_TOKEN = "<AUTH_TOKEN>"
TWILIO_PHONE_NUMBER = "<TWILIO_NUMBER>"
CUSTOMER_PHONE_NUMBER = "<CUSTOMER_NUMBER>"

# Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Mailbox
mailbox_lid_open = False

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Reed Switch on pin 18

# HX711 Setup
referenceUnit = 594
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()


def mailbox_is_open():
	return GPIO.input(18) == True


def mailbox_contents_weight():
	val = max(0.0, int(hx.get_weight(5)))
	hx.power_down()
	hx.power_up()
	time.sleep(0.1)
	print(f"grams: {val}")
	return val


def get_average_weight(number_of_references):
	return sum([mailbox_contents_weight() for i in range(number_of_references)]) / number_of_references


def get_date_time_stamp():
	return (datetime.now().strftime("%I:%M %p"), datetime.now().strftime("%B %d, %Y"))


def send_twilio_message(msg):
	print(msg)
	message = client.messages.create(body=msg, from_=TWILIO_PHONE_NUMBER, to=CUSTOMER_PHONE_NUMBER)
	print(message)


def send_mail_collected_notification():
	timestamp, datestamp = get_date_time_stamp()
	msg = f"\nYour Medical Package was collected at {timestamp} on {datestamp}. Mailbox Weight content is {str(round(get_average_weight(5) * 0.00220462, 2))}lbs."
	send_twilio_message(msg)


def send_mail_delivered_notification():
	timestamp, datestamp = get_date_time_stamp()
	msg = f"\nYour Medical Package arrived at {timestamp} on {datestamp}. Mailbox Weight content is {str(round(get_average_weight(5) * 0.00220462, 2))}lbs."
	send_twilio_message(msg)


def monitor_mailbox():
	try:
		weight_shift_tolerance = 100
		last_known_weight = get_average_weight(1)
		reset_needed = False
		print("Monitoring Started!")
		while True:
			content_weight = get_average_weight(1)
			mailbox_open = mailbox_is_open()
			if mailbox_open and not reset_needed:
				if content_weight - last_known_weight >= weight_shift_tolerance:
					send_mail_delivered_notification()
					reset_needed = True
				elif abs(content_weight - last_known_weight) >= weight_shift_tolerance:
					send_mail_collected_notification()
					reset_needed = True
				last_known_weight = content_weight
			if reset_needed and not mailbox_open:
				reset_needed = False
			time.sleep(0.2)
	except (Exception, KeyboardInterrupt) as e:
		GPIO.cleanup()
		print("\nprogram terminated")
		if e:
			print(e)


def main():
	monitor_mailbox()

if __name__ == '__main__':
	main()
