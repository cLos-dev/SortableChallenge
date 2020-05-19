import os,json,sys

# Note I fought the urge to objectify(model + assign) the common objects under the belief that the
# speed gained would be worth more, noting the mention of how many bids are run within a few
# seconds on live sites during the initial phone interview.
# if there are any questions regarding any other choices please feel free to ask
# I have documented the code to the extent of what I beleive should be easily understood by developers.

def main():
    config_dict = {}
    input_list = []
    # Attempting to retrieve config.json and convert
    try:
        with open('/auction/config.json') as json_config:
            config_dict = json.load(json_config)
    except FileNotFoundError:
        sys.exit("File not found, config.json expected")
    except json.decoder.JSONDecodeError:
        sys.exit("Invalid JSON provided in config, please check")
    except Exception as e:
        sys.exit(e)

    # Attempting to retrieve and convert input.json
    try:
        input_list = json.load(sys.stdin)
    except json.decoder.JSONDecodeError:
        sys.exit("Invalid JSON provided in input, please check")
    except Exception as e:
        sys.exit(e)

    run_auction(config_dict,input_list)


def run_auction(config_dict,input_list):
    winning_bids = []
    # For possible situation of multiple sites based on wording check each site
    for site in config_dict['sites']:
        # For possible multiple sites with multiple bids being placed
        for auction_input in input_list:
            # confirming that site is a valid site that is being bid on
            if auction_input['site'] == site['name']:
                # Going over the bids
                for bid in auction_input['bids']:
                    # Broke out validation of bidder for easier understanding and checked unit in bid is valid
                    if validateBidder(bid['bidder'],config_dict['bidders']) and bid['unit'] in auction_input['units']:
                        # Assigning value for easier readability
                        adjusted_bid = getAdjustedAmount(bid['bidder'],bid['bid'],config_dict['bidders'])
                        # Checking that the bid after doing adjustment is above floor for auction
                        if adjusted_bid > site['floor']:
                            # After confirming a valid unit checking to see if a bid already exists for unit
                            if not any(winning_bid['unit'] == bid['unit'] for winning_bid in winning_bids):
                                winning_bids.append(bid)
                            else:
                                for i in range(len(winning_bids)):
                                    winning_bid = winning_bids[i]
                                    # Checking if new bid on unit is greater than the previous with adjustment placed to both bids
                                    # if so remove previous bid and add new bid
                                    if winning_bids[i]['unit'] == bid['unit'] and adjusted_bid > getAdjustedAmount(winning_bid['bidder'],winning_bid['bid'],config_dict['bidders']):
                                        del winning_bids[i]
                                        winning_bids.append(bid)
                                        break # Break early if correct unit is found to avoid additional loops
    # Converting list to string to allow writing to stdout, if not valid bids or auctions and empty list will be output
    # This does allow printing out to to stdout for each site that is being bid on
    # if functionality was used, note that without understanding since output is based
    # on output.json there would be nothing to specify the site which in the real life situation
    # would be highly advisable
    sys.stdout.write(str(winning_bids))

# Quick check that the bidder is valid
def validateBidder(bidder_name,allowedBidders):
    if not any(bidder['name'] == bidder_name for bidder in allowedBidders):
        return False
    else:
        return True

# For code readability adjustment application and calculation removed from main script
def getAdjustedAmount(bidder_name,amount,allowedBidders):
    for bidder in allowedBidders:
        if bidder['name'] == bidder_name:
            return (amount * bidder['adjustment']) + amount

if __name__ == "__main__":
    main()