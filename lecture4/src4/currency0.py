import requests

def main():
    res = requests.get("https://api.fixer.io/latest?base=USD&symbols=EUR")
    if res.status_code != 200:
        pass#raise Exception("ERROR: API request unsuccessful.")
    res = "{'base':'USD','date':'2018-02-26','rates':{'EUR':0.81169}}"
    #data = res.json()
    print(eval(res))

if __name__ == "__main__":
    main()
