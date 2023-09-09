## Able to handle simple queries
`agent.run("can you list all the instrumentIds of Private Equity instruments?")` \
Returns: The instrumentIds of Private Equity instruments are: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 80, 81, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 130, 131, 132, 133, 134, 135, 140, 142, 143, 144, 146, 147, 149, 150, 151, 152, 153, 154, 155, 156, 157, 170, 171, 172, 173, 174, 175, 176, 177, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200]

## Able to handle complex queries
### As shown below, the way you prompt is very important
`agent.run("can you determine the total marketValue of Private Equity on 31/1/2020 12:00:00am?")` \
Failed this

`agent.run("on 31/1/2020 12:00:00am, can you determine the total marketValue of Private Equity?")` \
Returns: On January 31, 2020, at 12:00:00 AM, the total market value of Private Equity instruments was $50,792,525,962.09
Returns: On 31/1/2020 12:00:00am, the total market value of Private Equity is approximately $50,792,525,961.64

`agent.run("can you determine the total marketValue of Private Equity")` \
The total market value of private equity is approximately 1,925,806,433,825.

`agent.run("can you determine the total marketValue of Private Equity in the US")` \
Returns: The total market value of Private Equity in the US is approximately 554,953,316,165.56.
Returns: The total market value of private equity in the US is $554,953,316,171.875.