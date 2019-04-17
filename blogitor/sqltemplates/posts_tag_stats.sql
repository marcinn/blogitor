with tag_stats as (
    select unnest(tags) tag, count(*) cnt from blogitor_post
    {% if post_pks %}
    where id in ({{ post_pks|join:',' }})
    {% endif %}
    group by 1
), tag_buckets as (
    select
        width_bucket(cnt, 1, 3, 3) as bucket,
        int8range(min(cnt), max(cnt), '[]') bucket_range
    from tag_stats
    group by bucket
    order by bucket
)
select tag, cnt as freq, bucket as weight
from tag_stats, tag_buckets
where cnt <@ bucket_range
