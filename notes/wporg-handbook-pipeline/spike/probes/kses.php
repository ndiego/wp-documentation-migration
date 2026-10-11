<?php
var_dump(has_filter("content_save_pre","wp_filter_post_kses"), has_filter("title_save_pre","wp_filter_kses"), did_action("init"), did_action("set_current_user"), get_current_user_id());
