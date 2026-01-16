TRAIN_DATA = [
    (
        "Betaloc 100mg - 1 tab BID",
        {
            "entities": [
                (0, 7, "MED"),
                (8, 13, "STRENGTH"),
                (16, 21, "QTY"),
                (22, 25, "FREQ"),
            ]
        },
    ),
    (
        "Dorzolamidum 10 mg - 1 tab BID",
        {
            "entities": [
                (0, 12, "MED"),
                (13, 18, "STRENGTH"),
                (21, 26, "QTY"),
                (27, 30, "FREQ"),
            ]
        },
    ),
    (
        "Cimetidine 50 mg - 2 tabs TID",
        {
            "entities": [
                (0, 10, "MED"),
                (11, 16, "STRENGTH"),
                (19, 26, "QTY"),
                (27, 30, "FREQ"),
            ]
        },
    ),
    (
        "Oxprelol 50mg - 1 tab QD",
         {
            "entities": [
                (0, 8, "MED"),
                (9, 14, "STRENGTH"),
                (17, 22, "QTY"),
                (23, 25, "FREQ"),
            ]
        },
    ),
    # !!! ADD AT LEAST 20-50 MORE EXAMPLES FOR A DECENT MODEL !!!
]