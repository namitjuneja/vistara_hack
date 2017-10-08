from twitter import *
t = Twitter(
		        auth = OAuth(
		        				'845923993290887170-amXsT3U6aaHw5cJx3Mg5zQ0cbpJt0tz', 
		        				'Po250EXxr2Hs1EOCZ22vyMWRlPBH3YzVBlUn8wxQw9sgY', 
		        				't32qWI29icsvpny9Uh4cs3dHQ', 
		        				'ovemYqKnfLeSFPF3epXPf1A0ZWKQnCdFAwPuLwBiL5golu4MrS'
		        			)
		         )


a = t.search.tweets(q="#pycon", count=1, result_type='recent')
b = a['statuses'][0]['user']['screen_name']
print b
# for i in b.keys():
# 	print i, ":", b[i]