import math
from statistics import NormalDist
from scipy.stats import t

def ten_percent(samples):
    for i, sample in enumerate(samples):
        bign = int(input(f"Please estimate the size of sample {i + 1}'s population: "))
        if (sample > (0.10 * bign)):
            print(f"10% condition failed for sample {i + 1}. Continuing")
            return False
    return True

def large_counts(samples, phats):
    for i, sample, phat in enumerate(zip(samples, phats)):
        if (((sample * phat) < 10) or ((sample * (1-phat)) < 10)):
            print(f"Large counts failed for sample {i + 1}. Continuing")
            return False
    return True

def normal_large_sample(samples):
    res = []
    for i, sample in enumerate(samples):
        if sample >= 30:
            res.append(True)
        else:
            if(input("Is the population distribution normal (is it stated)? (y/n): ") == "y"):
                res.append(True)
            elif(input("Does the dotplot of the data show any large skew or obvious outliers? (y/n): ") == "n"):
                res.append(True)
            else:
                res.append(False)
    return all(res)

def one_sample_z_interval():
    print("### State ###")
    proportion = input("Please enter what the proportion would be (ex. the true proportion of...): ")
    clevel = float(input("Please enter the confidence level (without a percent sign): "))
    phat = float(input("Please enter your sample proportion (statistic) or p hat: "))
    ssize = int(input("Please enter the sample size used: "))
    print("### Plan ###")
    print("Method: One sample z-interval for p")
    print("Assuming the data is random...")
    print("Checking 10% condition...")
    tenpercent = ten_percent([ssize])
    print("Checking Large Counts Condition...")
    largecounts = large_counts([ssize], [phat])
    print("### Do ###")
    print("General formula: Point estimate ± Margin of error")
    print("Specific formula: p̂ ± z*√((p̂(1-p̂))/n)")
    zstar = NormalDist(mu=0, sigma=1).inv_cdf((clevel/2+50)/100)
    moe = zstar * math.sqrt((phat*(1-phat))/ssize)
    print(f"Interval: {phat} ± {round(moe, 3)}")
    print(f"Interval: ({round(phat - moe, 3)}, {round(phat + moe, 3)})")
    print("### Conclude ###")
    conclusion = f"We are {clevel}% confident that the interval from {round(phat - moe, 3)} to {round(phat + moe, 3)} captures {proportion}."
    print("")
    print(conclusion)

def two_sample_z_interval():
    print("Finding the confidence interval for p̂1 - p̂2")
    print("### State ###")
    context = input("Please the value trying to be found (ex. the true difference in proportions of...): ")
    clevel = float(input("Please enter the confidence level (without a percent sign): "))
    phat1 = float(input("Please enter the first sample proportion (p̂1): "))
    phat2 = float(input("Please enter the second sample proportion (p̂2): "))
    ssize1 = int(input("Please enter the sample size used for p̂1: "))
    ssize2 = int(input("Please enter the sample size used for p̂2: "))
    diff_phat = round(phat1 - phat2, 3)
    print(f"p̂1 - p̂2 = {diff_phat}")
    print("### Plan ###")
    print("Method: Two sample z-interval for p1-p2")
    print("Assuming the data is random and independent...")
    print("Checking 10% condition...")
    tenpercent = ten_percent([ssize1, ssize2])
    print("Checking Large Counts Condition...")
    largecounts = large_counts([ssize1, ssize2], [phat1, phat2])
    print("### Do ###")
    print("General formula: Point estimate ± Margin of error")
    print("Specific formula: (p̂1 - p̂2) ± z*√(((p̂1(1-p̂1))/n1) + ((p̂2(1-p̂2))/n2))")
    zstar = NormalDist(mu=0, sigma=1).inv_cdf((clevel/2+50)/100)
    moe = zstar * math.sqrt(((phat1*(1-phat1))/ssize1) + ((phat2*(1-phat2))/ssize2))
    print(f"Interval: {diff_phat} ± {round(moe, 3)}")
    low_interval = round(diff_phat - moe, 3)
    high_interval = round(diff_phat + moe, 3)
    print(f"Interval: ({low_interval}, {high_interval})")
    print("### Conclude ###")
    conclusion = f"We are {clevel}% confident that the interval from {low_interval} to {high_interval} captures the {context}."
    if(low_interval > 0 and high_interval > 0):
        convincing = "Since all values captured under the interval are greater than 0, we do have convincing evidence that p1 is greater than p2."
    elif(low_interval < 0 and high_interval < 0):
        convincing = "Since all values captured under the interval are less than 0, we do have convincing evidence that p2 is greater than p1."
    else:
        convincing = "Since the interval contains zero, is it plausible that there is no difference between the two populations."
    print("")
    print(conclusion)
    print(convincing)

def one_sample_t_interval():
    print("### State ###")
    mu = input("Please enter what the parameter would be (ex. the true mean...): ")
    clevel = float(input("Please enter the confidence level (without a percent sign): "))
    xbar = float(input("Please enter your sample mean (statistic): "))
    sx = float(input("Please enter your sample standard deviation: "))
    ssize = int(input("Please enter the sample size used: "))
    df = ssize - 1
    print(f"{df = }")
    print("### Plan ###")
    print("Method: One sample t-interval for μ")
    print("Assuming the data is random...")
    print("Checking 10% condition...")
    tenpercent = ten_percent([ssize])
    print("Checking Normal/Large Sample Condition...")
    normal = normal_large_sample([ssize])
    print("### Do ###")
    print("General formula: Point estimate ± Margin of error")
    print("Specific formula: x̄ ± t* (Sx/√n)")
    tstar = abs(t.isf((clevel/2+50)/100, df))
    moe = tstar * (sx/math.sqrt(ssize))
    print(f"Interval: {xbar} ± {round(moe, 3)}")
    print(f"Interval: ({round(xbar - moe, 3)}, {round(xbar + moe, 3)})")
    print("### Conclude ###")
    conclusion = f"We are {clevel}% confident that the interval from {round(xbar - moe, 3)} to {round(xbar + moe, 3)} captures {mu}."
    print("")
    print(conclusion)

def two_sample_t_interval():
    print("Finding the confidence interval for x̄1 - x̄2")
    print("### State ###")
    context = input("Please the value trying to be found (ex. the true difference in means of...): ")
    clevel = float(input("Please enter the confidence level (without a percent sign): "))
    xbar1 = float(input("Please enter the first sample mean (x̄1): "))
    xbar2 = float(input("Please enter the second sample mean (x̄2): "))
    sx1 = float(input("Please enter the standard deviation of x̄1: "))
    sx2 = float(input("Please enter the standard deviation of x̄2: "))
    ssize1 = int(input("Please enter the sample size used for x̄1: "))
    ssize2 = int(input("Please enter the sample size used for x̄2: "))
    df = (((sx1**2/ssize1)+(sx2**2/ssize2))**2)/(((sx1**2/ssize1)**2)/(ssize1-1) + ((sx2**2/ssize2)**2)/(ssize2-1))
    print(f"{df = }")
    diff_xbar = round(xbar1 - xbar2, 3)
    print(f"x̄1 - x̄2 = {diff_xbar}")
    print("### Plan ###")
    print("Method: Two sample t-interval for μ1-μ2")
    print("Assuming the data is random and independent...")
    print("Checking 10% condition...")
    tenpercent = ten_percent([ssize1, ssize2])
    print("Checking Large Counts Condition...")
    normal = normal_large_sample([ssize1, ssize2])
    print("### Do ###")
    print("General formula: Point estimate ± Margin of error")
    print("Specific formula: (x̄1 - x̄2) ± t*√((S1²/n1) + (S2²/n2))")
    tstar = abs(t.isf((clevel/2+50)/100, df))
    moe = tstar * math.sqrt((sx1**2/ssize1)+(sx2**2/ssize2))
    print(f"Interval: {diff_xbar} ± {round(moe, 3)}")
    low_interval = round(diff_xbar - moe, 3)
    high_interval = round(diff_xbar + moe, 3)
    print(f"Interval: ({low_interval}, {high_interval})")
    print("### Conclude ###")
    conclusion = f"We are {clevel}% confident that the interval from {low_interval} to {high_interval} captures the {context}."
    if(low_interval > 0 and high_interval > 0):
        convincing = "Since all values captured under the interval are greater than 0, we do have convincing evidence that μ1 is greater than μ2."
    elif(low_interval < 0 and high_interval < 0):
        convincing = "Since all values captured under the interval are less than 0, we do have convincing evidence that μ2 is greater than μ1."
    else:
        convincing = "Since the interval contains zero, is it plausible that there is no difference between the two populations."
    print("")
    print(conclusion)
    print(convincing)

def one_sample_t_interval_diff():
    print("### State ###")
    mudiff = input("Please enter what the parameter would be (ex. the true mean difference...): ")
    clevel = float(input("Please enter the confidence level (without a percent sign): "))
    xbardiff = float(input("Please enter your sample mean difference (statistic): "))
    sdiff = float(input("Please enter your sample standard deviation difference: "))
    ssize = int(input("Please enter the sample size used: "))
    df = ssize - 1
    print(f"{df = }")
    print("### Plan ###")
    print("Method: One sample t-interval for μdiff")
    print("Assuming the data is random...")
    print("Checking 10% condition...")
    tenpercent = ten_percent([ssize])
    print("Checking Normal/Large Sample Condition...")
    normal = normal_large_sample([ssize])
    print("### Do ###")
    print("General formula: Point estimate ± Margin of error")
    print("Specific formula: x̄diff ± t*(Sdiff/√n)")
    tstar = abs(t.isf((clevel/2+50)/100, df))
    moe = tstar * (sdiff/math.sqrt(ssize))
    low_interval = round(xbardiff - moe, 3)
    high_interval = round(xbardiff + moe, 3)
    print(f"Interval: {xbardiff} ± {round(moe, 3)}")
    print(f"Interval: ({low_interval}, {high_interval})")
    print("### Conclude ###")
    conclusion = f"We are {clevel}% confident that the interval from {low_interval} to {high_interval} captures {mudiff}."
    if(low_interval > 0 and high_interval > 0):
        convincing = "Since all plausible values are positive, we do have convincing evidence that A is greater than B."
    elif(low_interval < 0 and high_interval < 0):
        convincing = "Since all plausible values are negative, we do have convincing evidence that B is greater than A."
    else:
        convincing = "Since the interval contains zero, is it plausible that there is no difference."
    print("")
    print(conclusion)
    print(convincing)

print("Welcome to Max's Confidence Interval Calculator")
interval = input("Is this a confidence interval for proportions or means? (p or m): ")
if(interval.lower() == "p"):
    num_samples = int(input("How many samples are there?: "))
    if num_samples == 1:
        one_sample_z_interval()
    elif num_samples == 2:
        two_sample_z_interval()
    else:
        print("Invalid")
elif(interval.lower() == 'm'):
    num_samples = int(input("How many samples are there?: "))
    if num_samples == 1:
        isdiff = input("Is this an interval for mean difference? (y/n): ")
        if(isdiff.lower() == 'n'):
            one_sample_t_interval()
        elif(isdiff.lower() == 'y'):
            one_sample_t_interval_diff()
        else:
            print("Invalid")
    elif num_samples == 2:
        two_sample_t_interval()
    else:
        print("Invalid")
else:
    print("Please enter either 'p' or 'm'.")