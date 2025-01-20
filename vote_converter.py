def vote_converter(vote):
    if "K" in vote:
        vote = vote.replace("K", "")
        return float(vote) * 1000
    
    elif "M" in vote:
        vote = vote.replace("M", "")
        return float(vote) * 1000000
    
    else:
        return float(vote)