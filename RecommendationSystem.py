dataset = {
    'user1': {
        'silver spoon': 2.5,
        'gold spoon': 3.5,
        'Tupperware': 3.0,
        'Pillow': 3.5,
        'bedsheet': 2.5,
        'lamp': 3.0},

    'user2': {
        'silver spoon': 2.5,
        'gold spoon': 3.0,
        'Pillow': 3.5,
        'lamp': 4.0},

    'user3': {'lamp': 3.0,
              'TV': 4.0,
              'gold spoon': 2.0,
              'Pillow': 3.0,
              'silver spoon': 3.0,
              'LED light': 2.0},

    'user4': {'LED light': 3.0,
              'Pillow': 4.0,
              'lamp': 3.0,
              'silver spoon': 5.0,
              'gold spoon': 3.5},

    'user5': {'lamp': 4.5,
              'USB stick': 1.0,
              'TV': 4.0},

    'user6': {
        'Pillow': 3.0,
        'gold spoon': 3.5,
        'silver spoon': 1.5,
        'USB stick': 5.0,
        'LED light': 3.0,
        'lamp': 3.5},

    'user7': {'lamp': 3.5,
              'USB stick': 3.0,
              'LED light': 4.5,
              'gold spoon': 4.0,
              'TV': 2.5}}

from math import sqrt


def pearson_correlation(person1, person2):
    # To get both rated items
    both_rated = {}
    for item in dataset[person1]:
        if item in dataset[person2]:
            both_rated[item] = 1

    number_of_ratings = len(both_rated)

    # Checking for number of ratings in common
    if number_of_ratings == 0:
        return 0

    # Add up all the preferences of each user
    person1_preferences_sum = sum([dataset[person1][item] for item in both_rated])
    person2_preferences_sum = sum([dataset[person2][item] for item in both_rated])

    # Sum up the squares of preferences of each user
    person1_square_preferences_sum = sum([pow(dataset[person1][item], 2) for item in both_rated])
    person2_square_preferences_sum = sum([pow(dataset[person2][item], 2) for item in both_rated])

    # Sum up the product value of both preferences for each item
    product_sum_of_both_users = sum([dataset[person1][item] * dataset[person2][item] for item in both_rated])

    # Calculate the pearson score
    numerator_value = product_sum_of_both_users - (
                person1_preferences_sum * person2_preferences_sum / number_of_ratings)
    denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum, 2) / number_of_ratings) * (
                person2_square_preferences_sum - pow(person2_preferences_sum, 2) / number_of_ratings))
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r


def most_similar_users(person, number_of_users):
    # returns the number_of_users (similar persons) for a given specific person.
    scores = [(pearson_correlation(person, other_person), other_person) for other_person in dataset if
              other_person != person]

    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    scores.reverse()
    return scores[0:number_of_users]


def user_recommendations(person):
    # Gets recommendations for a person by using a weighted average of every other user's rankings
    totals = {}
    simSums = {}
    rankings_list = []
    for other in dataset:
        # don't compare me to myself
        if other == person:
            continue
        sim = pearson_correlation(person, other)
        # print ">>>>>>>",sim

        # ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in dataset[other]:

            # only score movies i haven't seen yet
            if item not in dataset[person] or dataset[person][item] == 0:
                # Similrity * score
                totals.setdefault(item, 0)
                totals[item] += dataset[other][item] * sim
                # sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Create the normalized list

    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    # returns the recommended items
    recommendataions_list = [recommend_item for score, recommend_item in rankings]
    return recommendataions_list


print(user_recommendations('user5'))
#print(similarity_score('user1','user3'))
print(pearson_correlation('user1', 'user2'))
print(most_similar_users('user1', 7))