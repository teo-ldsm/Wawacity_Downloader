def find_closest_title(list, title):
    closest_titles = []
    min_distance = float('inf')

    for cle in list:
        distance = levenshtein_distance(cle.lower(), title.lower())

        if distance < min_distance:
            min_distance = distance
            closest_titles = [cle]
        elif distance == min_distance:
            closest_titles.append(cle)

    if len(closest_titles) == 1:
        return closest_titles[0]
    
    min_distance = float("inf")
    closest_title = None
    for close_title in closest_titles:
        distance = distance_mot_a_mot(close_title, title)
        if distance < min_distance:
            min_distance = distance
            closest_title = close_title
    return closest_title

def levenshtein_distance(s, t):
    if s == t:
        return 0

    if len(s) == 0:
        return len(t)

    if len(t) == 0:
        return len(s)

    previous_row = range(len(t) + 1) # [0,1,...,23]
    for i, c1 in enumerate(s): # 0,h
        current_row = [i + 1] # [1]
        for j, c2 in enumerate(t): # 0,h 1,a
            insertions = previous_row[j + 1] + 1 # 2 
            deletions = current_row[j] + 1 # 1
            substitutions = previous_row[j] + (c1 != c2) # 0
            current_row.append(min(insertions, deletions, substitutions)) # [1,0]
        previous_row = current_row # [1,0]

    return previous_row[-1]

def distance_mot_a_mot(s, t):
    total_distance = 0
    for mot1 in s.split(" "):
        min_distance = float("inf")
        for mot2 in t.split(" "):
            distance = levenshtein_distance(mot1, mot2)
            # print(mot1, mot2, distance)
            if distance < min_distance:
                min_distance = distance
        total_distance += min_distance
    return total_distance

if __name__ == '__main__':
    titre_recherche = "harry potter reliques 2"
    titre_trouve_1 = "harry potter et les reliques de la mort - partie 1 (2010)"
    titre_trouve_2 = "harry potter et les reliques de la mort - partie 2 (2011)"
    titres_trouves = [titre_trouve_1, titre_trouve_2]
    assert find_closest_title(titres_trouves,titre_recherche) == titre_trouve_2

