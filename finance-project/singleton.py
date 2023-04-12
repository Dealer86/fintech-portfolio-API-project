def singleton(cls):
    instances = {}
    print("After declaration")
    print(instances)
    print(cls)

    def wrapper(*args, **kwargs):
        if cls not in instances:
            print(*args, **kwargs)
            instances[cls] = cls(*args, **kwargs)
        print("Before return")
        print(instances)
        return instances[cls]

    return wrapper


