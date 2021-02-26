categories = []
tasks = []
active_task = ""

if __name__ == "__main__":
    while True:
        ans = input("Would you like to (c)reate new task or (s)witch to another task? ")
        if ans == "c" or ans == "create":
            # category (subcategory)
            print(f"0 - New category")
            for i in range(1, len(categories)+1):
                print(f"{i} - {categories[i-1]}")
            ans = int(input())
            if ans == 0:
                category = input("New category name: ")
                categories.append(category)
            else:
                category = categories[ans-1]
            
            # task name
            task = input("New task name: ")
            tasks.append(task)

        elif ans == "s" or ans == "switch":
            # print categories (and subcategories)
            # print tasks
            # create time entry
            pass
        else:
            print("Invalid input")