from math import ceil


def batches(items, batch_size):

    total = len(items)

    for i in range(0, total, batch_size):

        yield items[i:i + batch_size]