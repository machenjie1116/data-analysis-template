df = read.csv('/home/oski/src/data-analysis-template/stat133proj2/errors.csv', header=F)
colnames(df) = c('Errors')
print(head(df))

df = read.csv('data/business_table.csv', header=F)
colnames(df) = c('business_id', 'name', 'review_count', 'rating', 'city', 'state')
print(head(df))

hist(df$rating, main='Review Rating Density Plot', prob=T)
curve(dnorm(x, mean=mean(df$rating), sd=sd(df$rating)), add=TRUE, col='red')

pie(table(df$state), main='Proportion of States')

plot((density(table(df$review_count))), main='Review Count Distribution')

plot(df$review_count, df$rating)
