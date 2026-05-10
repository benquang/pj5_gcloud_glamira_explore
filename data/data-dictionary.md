## Collection (summary):
__Fields__

- __[pica](https://nodeca.github.io/pica/demo/)__ - high quality and fast image
  resize in browser.
- __[babelfish](https://github.com/nodeca/babelfish/)__ - developer friendly
  i18n with plurals support and easy syntax.

- `_id` (ObjectId)
- `time_stamp` (int) – UNIX timestamp
- `ip` (string) – IPv4 address
- `user_agent` (string)
- `resolution` (string) – e.g., 375x667
- `user_id_db` (string)
- `device_id` (string UUID)
- `api_version` (string/number stored as string)
- `store_id` (string)
- `local_time` (string) – formatted datetime
- `show_recommendation` (string/bool-like; in example "false")
- `current_url` (string)
- `referrer_url` (string)
- `email_address` (string) (sensitive—don’t expose in public outputs)
- `recommendation` (boolean)
- `utm_source` / utm_medium (boolean-like; in example false)
- `collection` (string) – event name (the MongoDB collection / source)
- `product_id` (string, optional)
- `option` (array of objects)
- `option_label` (string)
- `option_id` (string)
- `value_label` (string, optional/empty)
- `value_id` (string, optional/empty)

You will like those projects!
