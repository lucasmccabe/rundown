# rundown

> Give me the rundown!

`rundown` is a WIP Twitter bot providing on-demand NLP features to newsreaders.

![box](img/logo_large.png)

Follow me on Twitter: [@rundown_bot](https://twitter.com/rundown_bot/with_replies)!

## Getting Started

Not currently live. May go live after articleabstract is complete.

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

## Contact
- Lucas McCabe ([email](mailto:lmccabe2@alumni.jh.edu))

## License
[MIT](https://choosealicense.com/licenses/mit/)
