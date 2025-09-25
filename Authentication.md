
# Authentication Guide (GraphQL API)

This document explains how to register, log in, log out, and use tokens with our GraphQL API. It is written for frontend developers working with Postman or Swagger-like tools.

---


## Table of Contents

- [Registration](#registration)
- [Login a User](#login-a-user)
- [Logout a User](#logout-a-user)
- [Refreshing Tokens](#refreshing-tokens)
- [Using Tokens for Protected Endpoints](#using-tokens-for-protected-endpoints)
- [Example Protected Query](#example-protected-query)
- [Summary](#summary)

## Registration

**Mutation**

```graphql
mutation {
  register(
    email: "user@example.com",
    username: "testuser",
    password1: "StrongPassword123!",
    password2: "StrongPassword123!"
  ) {
    success
    errors
    token
    refreshToken
  }
}
```
**Json Response**

```json
{
  "data": {
    "register": {
      "errors": null,
      "success": true,
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InlvbWFtYUBtYWlsLmNvbSIsImV4cCI6MTc1ODMwNzY2Miwib3JpZ0lhdCI6MTc1ODMwNjc2Mn0.-nq0tPH6y-DwQ35HiY4n7DcMmtio6LDkindvloMwVBw",
      "refreshToken": "d78368a79b62748d1c26a98c9782cd388470c03a"
    }
  }
}
```
- Only `email` and `password` are strictly required by our backend.
- On success, an activation email is sent (if configured).

---

## Login a User 
(Obtain Access & Refresh Tokens)

**Mutation**

```graphql
mutation {
  tokenAuth(email: "user@example.com", password: "StrongPassword123!") {
    success
    errors
    token  # Access token (short-lived, 15 minutes)
    refreshToken  # Refresh token (longer-lived, 14 days)
    payload   # contains user_id, username, etc.
  }
}
```
**Json Response**
```json
{
  "data": {
    "tokenAuth": {
      "success": true,
      "errors": null,
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InlvbWFtYUBtYWlsLmNvbSIsImV4cCI6MTc1ODMwNzg3Miwib3JpZ0lhdCI6MTc1ODMwNjk3Mn0.KjWtYLo-oh6-LfePCb90ffeKiuws0eorNH_aZ--epY0",
      "refreshToken": "ed8e11dc5a50e900e068e9a1deca988b3c5be053",
      "payload": {
        "email": "user@example.com",
        "exp": 1758307872,
        "origIat": 1758306972
      }
    }
  }
}
```
Save both `token` and `refreshToken`.

---

## Using Tokens for Protected Endpoints

- **Access Token** is required for queries/mutations that need authentication.
- Send it in the **HTTP header**:

```
Authorization: JWT <access_token>
```

⚠️ Note: Unlike typical REST APIs that use `Bearer`, this GraphQL API requires `JWT` as the prefix.

**Example (Postman Headers)**

| Key            | Value                    |
|-----------------|--------------------------|
| Content-Type    | application/json         |
| Authorization   | JWT eyJhbGciOiJIUzI1...  |

---

## Refreshing Tokens

When the access token expires, use the refresh token to obtain a new one.

**Mutation**

```graphql
mutation {
  refreshToken(refreshToken: "<your-refresh-token>") {
    token
    payload
  }
}
```
**Json Response**
```json
{
  "data": {
    "refreshToken": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InlvbWFtYUBtYWlsLmNvbSIsImV4cCI6MTc1ODMwODIxNCwib3JpZ0lhdCI6MTc1ODMwNzMxNH0.hUEf44X8_Bs14zr0YVkJo3bPJRNbKnQ0xJ9tT0COV6U",
      "payload": {
        "email": "user@example.com",
        "exp": 1758308214,
        "origIat": 1758307314
      }
    }
  }
}
```

This returns a new valid access token.

---

## Logout a User 
(Revoke Token)

To log out a user, revoke the refresh token:

**Mutation**

```graphql
mutation {
  revokeToken(refreshToken: "<your-refresh-token>") {
    revoked
  }
}
```
**Json Response**
```json
{
  "data": {
    "revokeToken": {
      "revoked": 1758307431,
      "success": true
    }
  }
}
```
Once revoked, the refresh token is invalid and cannot be used to generate new access tokens.

---

## Example Protected Query

```graphql
query{
  me{
    id
    username
    email
    isActive
    dateJoined
  }
}
```

**Json Response**
```json
{
  "data": {
    "me": {
      "id": "VXNlck5vZGU6MQ==",
      "username": "testuser",
      "email": "user@example.com",
      "isActive": true,
      "dateJoined": "2025-09-19T18:32:41.339501+00:00"
    }
  }
}
```

This will only work if you include access token in Request Headers:

```graphql
"Authorization": "JWT <access_token>"
```

---

## Summary

- Register → confirm account (if required).
- Login → get `access` + `refresh` tokens.
- Use `Authorization: JWT <access_token>` for all protected queries/mutations.
- Refresh token if access token expires.
- Revoke refresh token to log out.