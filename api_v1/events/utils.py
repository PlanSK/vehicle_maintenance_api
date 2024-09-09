from core.models import Event


async def get_average_mileage_interval(events_list: list[Event]) -> int:
    mileages_list = [event.mileage for event in events_list]
    event_counter = len(mileages_list)
    if event_counter <= 1:
        return 0
    previous_mileage = mileages_list[0]
    mileage_delta_sum = 0
    for mileage in mileages_list:
        mileage_delta_sum += mileage - previous_mileage
        previous_mileage = mileage
    return mileage_delta_sum // (event_counter - 1)
