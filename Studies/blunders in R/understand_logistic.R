# Load some sample data
admission <- read.csv("https://stats.idre.ucla.edu/stat/data/binary.csv")

# Make sure 'admit' is a factor. Reference level is 'no', target level is 'yes'
admission$admit <- factor( ifelse( admission$admit==1, "yes", "no" ) )

# Turn 'rank' into an unordered factor. This isn't realistic (it should be ordered) but
#	I just want an example for dummy coding
admission$rank <- factor( admission$rank, levels=4:1 )

# Show the proportions admitted for each rank
xtabs(~rank+admit, admission)[,2] / xtabs(~rank, admission)

