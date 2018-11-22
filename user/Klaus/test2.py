from law.preprocessing import read_law

crime01 = read_law("./data/Crime01.xlsx")
crime01.preprocess()
crime01.store("./data/r_Crime01.csv")
