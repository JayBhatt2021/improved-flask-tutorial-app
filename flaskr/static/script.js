/**
 * Prompts the user to confirm the deletion of a post
 */
const confirmDelete = () => {
    confirm('Are you sure?')
}

/**
 * Makes the background color of the upvote button lightgreen or white
 * if it was selected or deselected by the user, respectively
 *
 * @param  {String} buttonId The ID of the upvote button
 */
const pressUpvoteButton = (buttonId) => {
    const button = document.getElementById(buttonId)
    button.style.backgroundColor = button.style.backgroundColor === 'white' ? 'lightgreen' : 'white'
}
