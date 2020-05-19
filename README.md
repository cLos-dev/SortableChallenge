# Auction Coding Challenge

One of the things that the Engineering team at Sortable works on is software that
runs ad auctions, either in the browser or server-side. The goal of this challenge
is to write program that will run a simple auction, while enforcing data validity.

## General Approach

The language of choice was Python 3.8, libraries used were already present with the general installation of Python, as such Dockerfile was adjusted for the no longer required requirements.txt, elsewise for familarity in testing it was kept as would be familiar.

## Testing Method

Under the assumption that multiple config.json and input.json files would be used in testing I attempted multiple different files with adjusted, incorrect and specifically tailored values in order to confirm that expected results were returned.

## Example build and execution

```bash
$ docker build -t challenge .
$ docker run -i -v /path/to/challenge/config.json:/auction/config.json challenge < /path/to/challenge/input.json
```
