# multipli-lent
Repository for the Lent Multipli Hackbridge Project

Initially contains a prelimanry data cleaner, imputing values except those that are dates (this will hopefully be addressed later). Numerical datatypes are fille with the column modes and strings are replaced with "unknown". Later stages could include more advanced imputing strategies such as MICE, but this should be sufficient for preliminary experimentation. Data is retrieved from the data/original directory and stored as a pkl file in data/processed. To open this please use pandas.read_pickle.

Developer note:
Please createe your own branch when working on this project using:

git checkout -b insert-your-name
