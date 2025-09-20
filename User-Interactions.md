# User Profiles & Social Interactions (GraphQL API)

This document explains how users can update their profiles, follow/unfollow each other, and query user relationships using our GraphQL API.  

⚠️ **Note**: All these mutations and queries require authentication via a valid **JWT access token**. Include it in your headers:  

```
Authorization: JWT <access_token>
```

---

## Table of Contents

- [Update User Profile](#update-user-profile)
- [Follow a User](#follow-a-user)
- [Unfollow a User](#unfollow-a-user)
- [Query Users and Their Relationships](#query-users-and-their-relationships)
- [Summary](#summary)

## Update User Profile

**Mutation**

```graphql
mutation {
  updateProfile(
    bio: "This is my first new bio yoh!"
    location: "Nairobi"
    profilePic: "https://example.com/profile.png"
  ) {
    success
    message
    profile {
      id
      bio
      profilePic
      location
      birthDate
    }
  }
}
```

**Example JSON Response**

```json
{
  "data": {
    "updateProfile": {
      "success": true,
      "message": "Profile updated successfully.",
      "profile": {
        "id": "1",
        "bio": "This is my first new bio yoh!",
        "profilePic": "https://example.com/profile.png",
        "location": "Nairobi",
        "birthDate": null
      }
    }
  }
}
```

---

## Follow a User

**Mutation**

```graphql
mutation {
  followUser(userId: 2) {
    success
    message
    follower {
      id
      username
      dateJoined
    }
    followed {
      id
      username
      dateJoined
    }
  }
}
```

**Example JSON Response**

```json
{
  "data": {
    "followUser": {
      "success": true,
      "message": null,
      "follower": {
        "id": "1",
        "username": "testuser1",
        "dateJoined": "2025-09-19T18:32:41.339501+00:00"
      },
      "followed": {
        "id": "2",
        "username": "testuser2",
        "dateJoined": "2025-09-15T14:12:11.000000+00:00"
      }
    }
  }
}
```

---

## Unfollow a User

**Mutation**

```graphql
mutation {
  unfollowUser(userId: 2) {
    success
    message
    follower {
      id
      username
    }
    unfollowed {
      id
      username
    }
  }
}
```

**Example JSON Response**

```json
{
  "data": {
    "unfollowUser": {
      "success": true,
      "message": "User unfollowed successfully.",
      "follower": {
        "id": "1",
        "username": "testuser1"
      },
      "unfollowed": {
        "id": "2",
        "username": "testuser2"
      }
    }
  }
}
```

---

## Query Users and Their Relationships

**Query**

```graphql
query {
  users {
    edges {
      node {
        id
        pk
        username
        email
        followers {
          follower {
            id
            username
            profile {
              id
              bio
            }
          }
        }
        following {
          follower {
            id
            username
            profile {
              id
              bio
            }
          }
        }
      }
    }
  }
}
```

**Example JSON Response**

```json
{
  "data": {
    "users": {
      "edges": [
        {
          "node": {
            "id": "1",
            "pk": 1,
            "username": "testuser1",
            "email": "user1@example.com",
            "followers": [
              {
                "follower": {
                  "id": "2",
                  "username": "testuser2",
                  "profile": {
                    "id": "2",
                    "bio": "I follow user1!"
                  }
                }
              }
            ],
            "following": []
          }
        }
      ]
    }
  }
}
```

---

## Important Note on `id` vs `pk`

When performing follow/unfollow mutations, you must pass the **user’s `pk` (primary key)** as the `userId` argument.  

- The `id` field you see in queries (e.g., `"id": "VXNlck5vZGU6MQ=="`) is a **base64-encoded global ID string**, not an integer.  
- The GraphQL schema expects an integer for `userId`.  

**Example**

```graphql
mutation {
  followUser(userId: 1) {
    success
    message
    follower {
      id
      username
    }
    followed {
      id
      username
    }
  }
}
```

So when querying users, make sure you include the `pk` field in your query to get the correct integer ID to use in mutations.

```graphql
query {
  users {
    edges {
      node {
        id
        pk   # Use this for follow/unfollow mutations
        username
      }
    }
  }
}
```

---

## Summary

- **Update Profile** → Change bio, picture, location, or birth date.  
- **Follow/Unfollow** → Manage user relationships.  
- **Query Users** → Fetch users with their followers and following lists.  