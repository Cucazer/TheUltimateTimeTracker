categories = []

if __name__ == "__main__":
    while True:
        ans = input("Would you like to (c)reate new task or (s)witch to another task? ")
        if ans == "c" or ans == "create":
            # category (subcategory)
            i = 0
            for i in range (len(categories)):
                print(f"{i} - {categories[i]}")
            print(f"{i+1} - New category")
            ans = int(input())
            if ans < len(categories):
                pass
            elif ans == len(categories):
                ans = input("New category name: ")
            else:
                print("Invalid input")
            # task name
            pass
        elif ans == "s" or ans == "switch":
            # print categories (and subcategories)
            # print tasks
            # create time entry
            pass
        else:
            print("Invalid input")