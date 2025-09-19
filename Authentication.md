
# Authentication Guide (GraphQL API)

This document explains how to register, log in, log out, and use tokens with our GraphQL API. It is written for frontend developers working with Postman or Swagger-like tools.

---

## 1. Registration

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
  }
}
```

- Only `email` and `password` are strictly required by our backend.
- On success, an activation email is sent (if configured).

---

## 2. Login (Obtain Access & Refresh Tokens)

**Mutation**

```graphql
mutation {
  tokenAuth(username: "user@example.com", password: "StrongPassword123!") {
    success
    errors
    token  # Access token (short-lived, 15 minutes)
    refreshToken  # Refresh token (longer-lived, 14 days)
    payload   # contains user_id, username, etc.
  }
}
```

Save both `token` and `refreshToken`.

---

## 3. Using Tokens for Protected Endpoints

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

## 4. Refreshing Tokens

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

This returns a new valid access token.

---

## 5. Logout (Revoke Token)

To log out a user, revoke the refresh token:

```graphql
mutation {
  revokeToken(refreshToken: "<your-refresh-token>") {
    revoked
  }
}
```

Once revoked, the refresh token is invalid and cannot be used to generate new access tokens.

---

## 6. Example Protected Query

```graphql
query {
  me {
    username
    email
    isActive
  }
}
```

This will only work if you include:

```
Authorization: JWT <access_token>
```

---

## Summary

- Register → confirm account (if required).
- Login → get `access` + `refresh` tokens.
- Use `Authorization: JWT <access_token>` for all protected queries/mutations.
- Refresh token if access token expires.
- Revoke refresh token to log out.