import math
import time

def difficulty(last_block_timestamp, block_minus_1_timestamp, block_minus_1_difficulty, block_minus_1441_timestamp):
    #this is a simplified version that only works in the land of gnomes and fairies

    block_time_prev = (block_minus_1_timestamp - block_minus_1441_timestamp) / 1440
    timestamp_1440 = block_minus_1441_timestamp
    block_time = (last_block_timestamp - timestamp_1440) / 1440

    time_to_generate = last_block_timestamp - block_minus_1_timestamp

    hashrate = pow(2, block_minus_1_difficulty / (2.0)) / (
            block_time * math.ceil(28 - block_minus_1_difficulty / (16.0)))
    # Calculate new difficulty for desired blocktime of 60 seconds
    target = (60.00)
    ##D0 = diff_block_previous
    difficulty_new = (
        (2 / math.log(2)) * math.log(hashrate * target * math.ceil(28 - block_minus_1_difficulty / (16.0))))
    # Feedback controller
    Kd = 10
    difficulty_new = difficulty_new - Kd * (block_time - block_time_prev)
    diff_adjustment = (difficulty_new - block_minus_1_difficulty) / 720  # reduce by factor of 720

    if diff_adjustment > (1.0):
        diff_adjustment = (1.0)

    difficulty_new_adjusted = (block_minus_1_difficulty + diff_adjustment)
    difficulty = difficulty_new_adjusted

    diff_drop_time = (180)

    if (time.time()) > (last_block_timestamp) + (2 * diff_drop_time):
        # Emergency diff drop
        time_difference = (time.time()) - (last_block_timestamp)
        diff_dropped = (difficulty) - (1) \
                       - (10 * (time_difference - 2 * diff_drop_time) / diff_drop_time)
    elif (time.time()) > (last_block_timestamp) + (diff_drop_time):
        time_difference = (time.time()) - (last_block_timestamp)
        diff_dropped = (difficulty) + (1) - (time_difference / diff_drop_time)
    else:
        diff_dropped = difficulty

    if difficulty < 50:
        difficulty = 50
    if diff_dropped < 50:
        diff_dropped = 50

    return {
        "difficulty" : float(difficulty),
        "diff_dropped" : float(diff_dropped),
        "time_to_generate" : float(time_to_generate),
        "difficulty_previous" : float(block_minus_1_difficulty),
        "block_time" : float(block_time),
        "hashrate" : float(hashrate),
        "diff_adjustment" : float(diff_adjustment)}  # need to keep float here for database inserts support

if __name__ == "__main__":
    print (difficulty(time.time(),time.time()-60,109,time.time()-1440*60))