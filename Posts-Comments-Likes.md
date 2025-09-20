# Post Features Documentation

## Table of Contents
- [Posts](#posts)
- [Comments](#comments)
- [Nested Comments](#nested-comments)
- [Likes](#likes)
- [Mutations Overview](#mutations-overview)

---

## Posts

### Queries
- **Get all posts**
```graphql
query {
  posts {
    id
    title
    content
    mediaUrl
    createdAt
    author {
      id
      username
    }
  }
}
```

- **Get a single post**
```graphql
query {
  post(id: 1) {
    id
    title
    content
    createdAt
  }
}
```

### Mutations
- **Create a post**
```graphql
mutation {
  createPost(title: "My first post", content: "Hello world!", mediaUrl: "") {
    success
    message
    post {
      id
      title
      content
    }
  }
}
```

- **Delete a post**
```graphql
mutation {
  deletePost(postId: 1) {
    success
    message
  }
}
```

---

## Comments

### Queries
- **Get comments for a post**
```graphql
query {
  commentsPost(postId: 1) {
    id
    content
    author {
      username
    }
  }
}
```

- **Count comments on a post**
```graphql
query {
  commentsCount(postId: 1)
}
```

### Mutations
- **Create a comment on a post**
```graphql
mutation {
  createComment(postId: 1, content: "Nice post!") {
    success
    message
    comment {
      id
      content
    }
  }
}
```

- **Delete a comment**
```graphql
mutation {
  deleteComment(commentId: 1) {
    success
    message
  }
}
```

---

## Nested Comments

### Mutations
- **Create a comment on a comment (nested comment)**
```graphql
mutation {
  createCommentComment(parentCommentId: 1, content: "Replying to your comment") {
    success
    message
    comment {
      id
      content
    }
  }
}
```

- **Delete a nested comment**
```graphql
mutation {
  deleteCommentComment(commentId: 2) {
    success
    message
  }
}
```

---

## Likes

### Queries
- **Get likes for a post**
```graphql
query {
  likesPost(postId: 1) {
    id
    user {
      username
    }
  }
}
```

- **Count likes on a post**
```graphql
query {
  likeCount(postId: 1)
}
```

- **Get likes for a comment**
```graphql
query {
  likesComment(commentId: 1) {
    id
    user {
      username
    }
  }
}
```

- **Count likes on a comment**
```graphql
query {
  likeCountComment(commentId: 1)
}
```

### Mutations
- **Like a post**
```graphql
mutation {
  createLikePost(postId: 1) {
    success
    message
    like {
      id
      post {
        id
      }
    }
  }
}
```

- **Unlike a post**
```graphql
mutation {
  unlikePost(postId: 1) {
    success
    message
  }
}
```

- **Like a comment**
```graphql
mutation {
  createLikeComment(commentId: 1) {
    success
    message
    like {
      id
      comment {
        id
      }
    }
  }
}
```

- **Unlike a comment**
```graphql
mutation {
  unlikeComment(commentId: 1) {
    success
    message
  }
}
```

---

## Mutations Overview
✅ **Posts** → Create, Delete  
✅ **Comments** → Create, Delete  
✅ **Nested Comments** → Create, Delete  
✅ **Likes** → Create/Unlike for both posts and comments  