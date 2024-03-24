#! /bin/bash

LANGUAGE=$1 # heb, gk-ot
VERSE=$2 # for api.bible: GEN.1.1; for bible-api: joannes+3:16

if [ "$LANGUAGE" == "heb" ]; then
    BIBLE_ID=2c500771ea16da93-01
    API=API.BIBLE
elif [ "$LANGUAGE" == "gk-ot" ]; then
    BIBLE_ID=c114c33098c4fef1-01
    API=API.BIBLE
elif [ "$LANGUAGE" == "la" ]; then
    API=BIBLE_API
else
    echo "Language not supported"
    exit 1
fi

if [ "$API" == "API.BIBLE" ]; then
    curl -s --header "api-key: $API_BIBLE_KEY" \
        "https://api.scripture.api.bible/v1/bibles/$BIBLE_ID/verses/$VERSE" | \
        jq -r .data.content | cut -d '>' -f 4 | cut -d '<' -f 1
elif [ "$API" == "BIBLE_API" ]; then
    curl -s "https://bible-api.com/$VERSE?translation=clementine" | \
        jq -r '.verses[0].text'
fi