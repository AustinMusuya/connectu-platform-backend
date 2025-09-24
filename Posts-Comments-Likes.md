# Post Features Documentation

## Table of Contents
- [Posts](#posts)
- [Comments](#comments)
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
    commentCount
    likeCount
    author {
      username
    }
    comments {
      id
      content
      likeCount
      author {
        username
      }
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
    commentCount
    likeCount
    author {
      username
    }
    comments {
      id
      content
      likeCount
      author {
        username
      }
    }
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
      likeCount
      commentCount
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
- **Comments are nested under posts now**  
(see `posts { comments { ... } }` above).  

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
      likeCount
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

- **Create a nested comment (reply)**
```graphql
mutation {
  createCommentComment(parentCommentId: 1, content: "Replying to your comment") {
    success
    message
    comment {
      id
      content
      likeCount
    }
  }
}
```

- **Delete a nested comment**
```graphql
mutation {
  deleteComment(commentId: 2) {
    success
    message
  }
}
```

---

## Likes

### Queries
- **Likes are now exposed as `likeCount` on posts and comments**  
(see queries above).  

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
        likeCount
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
        likeCount
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