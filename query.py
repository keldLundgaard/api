from collections import defaultdict

def documents_browse_news_articles_source(es, domains, text, histogram, skip, limit, mindate, maxdate):
    q = {
        "from": skip,
        "size": limit,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "extracted.date": {
                                "gte": mindate,
                                "lte": maxdate
                            }
                        }
                    }
                ]
            }
        }
    }
    if text is not None:
        q["query"]["bool"]["must"].append({
            "match": {
                "extracted.text": text
            }
        })
    if len(domains) > 0:
        q["query"]["bool"]["must"].append({
            "terms": {
                "source.url": domains
            }
        })
    if histogram is True:
        q["aggs"] = {
            "dates": {
                "date_histogram": {
                    "field": "extracted.date",
                    "calendar_interval": "day",
                    "time_zone": "America/New_York"
                }
            }
        }
        response = es.search(index="news_articles", body=q, filter_path=["aggregations"])
        try:
            return response["aggregations"]["dates"]["buckets"]
        except:
            return []
    else:
        response = es.search(index="news_articles", body=q, filter_path=["hits.hits._id", "hits.hits._source.extracted.title", "hits.hits._source.extracted.text", "hits.hits._source.extracted.date", "hits.hits._source.url"])
        try:
            return response["hits"]["hits"]
        except:
            return []

def documents_browse_twitter_tweets_user(es, user_ids, text, histogram, skip, limit, mindate, maxdate):
    q = {
        "from": skip,
        "size": limit,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "obj.created_at": {
                                "gte": mindate,
                                "lte": maxdate
                            }
                        }
                    }
                ]
            }
        }
    }
    if text is not None:
        q["query"]["bool"]["must"].append({
            "match": {
                "obj.text": text
            }
        })
    if len(user_ids) > 0:
        q["query"]["bool"]["must"].append({
            "terms": {
                "user_id": user_ids
            }
        })
    if histogram is True:
        q["aggs"] = {
            "dates": {
                "date_histogram": {
                    "field": "obj.created_at",
                    "calendar_interval": "day",
                    "time_zone": "America/New_York"
                }
            }
        }
        response = es.search(index="twitter_tweets,tweets_old", body=q, filter_path=["aggregations"])
        try:
            return response["aggregations"]["dates"]["buckets"]
        except:
            return []
    else:
        response = es.search(index="twitter_tweets,tweets_old", body=q, filter_path=["hits.hits._source.user_id", "hits.hits._source.user_screen_name", "hits.hits._source.obj.id", "hits.hits._source.obj.created_at", "hits.hits._source.obj.entities.hashtags"])
        try:
            return response["hits"]["hits"]
        except:
            return []

def documents_browse_facebook_ads(es, text, histogram, skip, limit, mindate, maxdate):
    q = {
        "from": skip,
        "size": limit,
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {
                                    "range": {
                                        "obj.ad_creation_time": {
                                            "gte": mindate,
                                            "lte": maxdate
                                        }
                                    }
                                },
                                {
                                    "range": {
                                        "obj.created": {
                                            "gte": mindate,
                                            "lte": maxdate
                                        }
                                    }
                                }
                            ],
                            "minimum_should_match": 1
                        }
                    }
                ]
            }
        }
    }
    if text is not None:
        q["query"]["bool"]["must"].append({
            "bool": {
                "should": [
                    {
                        "match": {
                            "obj.ad_creative_body": text
                        }
                    },
                    {
                        "match": {
                            "obj.ad_creative_link_description": text
                        }
                    },
                    {
                        "match": {
                            "obj.title": text
                        }
                    },
                    {
                        "match": {
                            "obj.selftext": text
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        })
    if histogram is True:
        q["aggs"] = {
            "facebook": {
                "date_histogram": {
                    "field": "obj.ad_creation_time",
                    "calendar_interval": "day",
                    "time_zone": "America/New_York"
                }
            }
        }
        response = es.search(index="facebook_ads", body=q, filter_path=["aggregations"])
        try:
            buckets = defaultdict(lambda : {"key_as_string": "", "key": 0, "doc_count": 0})
            for d in response["aggregations"]["facebook"]["buckets"]:
                buckets[d["key_as_string"]]["key_as_string"] = d["key_as_string"]
                buckets[d["key_as_string"]]["key"] = d["key"]
                buckets[d["key_as_string"]]["doc_count"] += d["doc_count"]
            return [v for k,v in buckets.items()]
        except:
            return []
    else:
        response = es.search(index="facebook_ads", body=q, filter_path=["hits.hits._source.type", "hits.hits._source.obj.id", "hits.hits._source.obj.page_id", "hits.hits._source.obj.page_name", "hits.hits._source.obj.funding_entity", "hits.hits._source.obj.permalink", "hits.hits._source.obj.ad_creation_time", "hits.hits._source.obj.created"])
        try:
            return response["hits"]["hits"]
        except:
            return []
