from datetime import datetime, time, timedelta

def available(cafe_branch):
	checkout_times = all_slots(cafe_branch)
	now = datetime.now().time()
	available_slots = []
	for slot in checkout_times:
		if slot > now:
			available_slots.append(slot)
	return available_slots


def all_slots(cafe_branch):
	starting = add_time(cafe_branch.opening_time , time(minute=30))
	finishing = rem_time(cafe_branch.closing_time, time(hour=1))

	checkout_times = [starting]
	time_slot = starting
	while True:
		time_slot = add_time(time_slot, time(minute=45))
		if time_slot > finishing:
			break
		if time_slot.minute == 0:
			continue
		checkout_times.append(time_slot)
	return checkout_times


def add_time(base_time, block_time):
	time_delta = (
		timedelta(hours=base_time.hour, minutes=base_time.minute, seconds=base_time.second)
		+
		timedelta(hours=block_time.hour, minutes=block_time.minute, seconds=block_time.second)
	)
	return to_time(time_delta)


def rem_time(base_time, block_time):
	time_delta = (
		timedelta(hours=base_time.hour, minutes=base_time.minute, seconds=base_time.second)
		-
		timedelta(hours=block_time.hour, minutes=block_time.minute, seconds=block_time.second)
	)
	return to_time(time_delta)


def to_time(time_delta):
	split_list = str(time_delta).split(':')
	return time(hour=int(split_list[0]),
		minute=int(split_list[1]),
		second=int(split_list[2]))