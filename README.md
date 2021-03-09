# rundown

`rundown` is a WIP Twitter bot to help resolve the social media information bottleneck.

![box](img/logo_large.PNG)

Find me on Twitter: [@rundown_bot](https://twitter.com/rundown_bot/with_replies)!

## Usage

#### Current functionality:

- Command: doesfollow
  - Format: @rundown_bot #doesfollow @user1 @user2
  - Function: inquires if user1 follows user2
- Command: articlepeople
  - Format: @rundown_bot #articlepeople url
  - Function: extracts named entities tagged PERSON from linked article
- Command: articleplaces
  - Format: @rundown_bot #articleplaces url
  - Function: extracts named entities tagged GPE from linked article
- Command: articleorgs
  - Format: @rundown_bot #articleorgs url
  - Function: extracts named entities tagged ORGANIZATION from linked article

#### WIP functionality:

- Command: articleabstract
  - Format: @rundown_bot #articleabstract url
  - Function: abstractive summarization of linked article

## License
[MIT](https://choosealicense.com/licenses/mit/)
