# /user

Retrieve messages

## POST
+ Response 200 (text/plain)

        Hello World!
        Hello Other World


# /user/{id}
Represents a particular message by it's *id*.

## Retrieve message [POST]
+ Response 200 (text/plain)



{
  "status_describe":"success add user"
}

+ Response 403 (text/plain)
{

  "status_describe":"post body has not allow field {var}."

}


## DELETE MESSAGE DELETE
+ Response 204

# /user/{id}.json

## Retrieve message in JSON [POST]
+ Response 200 (application/json)

        {"message": "Hello World!"}




# /user

Retrieve messages

## GET
+ Response 200 (text/plain)

        Hello World!
        Hello Other World


# /user/{id}
Represents a particular message by it's *id*.

## Retrieve message [GET]
+ Response 200 (text/plain)



{
  "user_open_id":"abcDemo",
  "user_nick_name":"yoyo",
  "user_status" : "haha",
  "user_img" : "https://ddascd",
  "user_register_date" :  153030394,
  "user_register_menu" : "xxxxxxx"
}


## DELETE MESSAGE DELETE
+ Response 204

# /user/{id}.json

## Retrieve message in JSON [GET]
+ Response 200 (application/json)


{
  "status_describe":"success add user"
}



# /user

Retrieve messages

## PUT
+ Response 200 (text/plain)

        Hello World!
        Hello Other World


# /user/{id}
Represents a particular message by it's *id*.

## Retrieve message [PUT]
+ Response 200 (text/plain)



{
    "user_nick_name":"yoyo",
    "user_status" : "haha",
    "user_img" : "https://ddascd",
    "user_register_menu" : "xxxxxxx"
}



## DELETE MESSAGE DELETE
+ Response 204

# /user/{id}.json

## Retrieve message in JSON [PUT]
+ Response 200 (application/json)


{
  "status_describe":"success add user"
}




# /users

Retrieve messages

## GET
+ Response 200 (text/plain)

        Hello World!
        Hello Other World


# /users/{id}
Represents a particular message by it's *id*.

## Retrieve message [GET]
+ Response 200 (text/plain)





{
    "user_open_id":"abcDemo",
    "user_nick_name":"yoyo",
    "user_status" : "haha",
    "user_img" : "https://ddascd",
    "user_register_date" :  153030394,
    "user_register_menu" : "xxxxxxx"
}



## DELETE MESSAGE DELETE
+ Response 204

# /users/{id}.json

## Retrieve message in JSON [GET]
+ Response 200 (application/json)


{
  "status_describe":"success add user"
}



# /question/sa

Retrieve messages

## GET
+ Response 200 (text/plain)



{
    "user_open_id":"abcDemo",
    "user_nick_name":"yoyo",
    "user_status" : "haha",
    "user_img" : "https://ddascd",
    "user_register_date" :  153030394,
    "user_register_menu" : "xxxxxxx"
}



# /question/develop

Retrieve messages

## GET
+ Response 200 (text/plain)




{
  "question_id":1,
  "question_content":"how are you",
  "answer1_content":"fine",
  "answer2_content":"soso",
  "answer3_content":"great",
  "answer4_content":"bad",
  "true_answer":1,
  "true_answer_decribe_content" : "life is great",
  "external_link": ""
}




# /menu

Retrieve messages

## POST
+ Response 200 (text/plain)



{
  "question_id":1,
  "question_content":"menu how are you",
  "answer1_content":"fine",
  "answer2_content":"sysops",
  "answer3_content":"great",
  "answer4_content":"bad",
  "true_answer":1,
  "true_answer_decribe_content" : "life is great",
  "external_link": ""
}





# /menu
Represents a particular message by it's *id*.

## Retrieve message [POST]
+ Response 200 (text/plain)



{
  "status_describe":"success add menu"
}


## DELETE MESSAGE DELETE
+ Response 204

# /menu.json

## Retrieve message in JSON [POST]
+ Response 200 (application/json)


{
  "status_describe":"success add user"
}



