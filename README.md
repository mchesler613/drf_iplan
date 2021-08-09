# drf_iplan
drf_iplan is the DRF APIs for the `iplan` project. 

## Django Packages
$ pip install djangorestframework

## The main endpoints

+ /people - list the `Person` model instances, connected with a `User`
+ /tasks - list all `Task` model instances
+ /tasks/people/pk - list the `Task` model instances, connected with a `Person` based on pk
+ /meetings - list all `Meeting` model instances
+ /meetings/people/pk - list the `Meeting` model instances, connected with a `Person` based on pk

## Order of Operations
1. Create a `User`. (currently disabled)
2. Login as `User`.
3. Create a `Person` associated with `User`.
4. Create a `Task` associated with `Person`.
5. Create a `Meeting` associated with `Person`.

## List/Create a User (Currently disabled)
+ To list all `User`s, or create a new `User`, use `/users`.

## Update/Delete User
This can only be done once logged in. 
+ To update/delete a `User`, use `/users/<pk>` where `pk` is the id of the `User`. 

## List/Create/Update/Delete a Person
A `Person` is associated with a Django `User`. To create/update/delete a `Person` requires logging in as a `User`. 
+ To list all `Person`s (people), or create a `Person`, use `/people`.
+ To update/delete a particular `Person`, use `/people/<pk>` where `pk` is the id of the `Person`.

## List/Create/Update/Delete a Task
A `Task` is associated with a `Person`. 
+ To create/update/delete a `Task` requires logging in as a valid `User` who is associated with a `Person`.
+ To create a new `Task` for any `Person`, use `/tasks`.
+ To list `Task`s associated with a `Person`, use `/tasks/people/<pk>` where `pk` is the id of the `Person`.
+ To update/delete a `Task` use `/tasks/<pk>` where `pk` is the `Task` id, however, only the owner of the task who is the `Person` associated with the `User` has access to this operation.

## List/Create/Update/Delete a Meeting
A `Meeting` is associated with a `Person`. 
+ To create/update/delete a `Meeting` requires logging in as a valid `User` who is associated with a `Person`.
+ To create a new `Meeting` for any `Person`, use `/meetings`.
+ To list `Meeting`s associated with a `Person`, use `/meetings/people/<pk>` where `pk` is the id of the `Person`.
+ To update/delete a `Meeting` use `/meetings/<pk>` where `pk` is the `Meeting` id, however, only the creator of the task who is the `Person` associated with the `User` has access to this operation.
