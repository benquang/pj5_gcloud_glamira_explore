## Collection (summary):
__Fields__

- `_id` (ObjectId)
- `time_stamp` (int) – UNIX timestampz
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


_Product id rule (important for step 6)__

- `product_id` if present.
- else use `viewing_product_id`
