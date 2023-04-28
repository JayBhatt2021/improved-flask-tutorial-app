/**
 * index.js
 *
 * This file provides the JS functionality for this project.
 */

/**
 * Handles the events associated with pressing the upvote button of a post
 *
 * @param  {String} postId The ID of the post.
 */
function upvote(postId) {
  // Obtains the upvote button and its count, respectively
  const upvoteButton = document.getElementById(`upvote-button-${postId}`);
  const upvoteCount = document.getElementById(`upvotes-count-${postId}`);

  fetch(`/upvote/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((resData) => {
      // Sets the upvote count
      upvoteCount.innerHTML = `${resData["upvoteCount"]} Upvotes`;

      // Sets the background color based on whether the user upvoted the post
      if (resData["isUpvotedByCurrentUser"] === true) {
        upvoteButton.style.backgroundColor = "lightgreen";
      } else {
        upvoteButton.style.backgroundColor = "white";
      }
    })
    .catch((_) => alert("You must be signed in to upvote a post."));
}
