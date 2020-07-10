window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

// const modal = document.getElementById("myModal");
// const span = document.getElementsByClassName("close")[0];
// const deleteBtn = document.getElementById("deleteBtn");
// const cancelDelete = document.getElementsByClassName("cancel-delete-btn")[0];
//
//
// // deleteBtn.onclick = () => {
// //   modal.style.display = "block";
// // }
//
// span.onclick = () => {
//   modal.style.display = "none";
// }
//
// cancelDelete.onclick = () => {
//   modal.style.display = "none";
// }


// document.getElementById('new-artist-form').onsubmit = (e) => {
//   e.preventDefault();
//
//   fetch('artists/create', {
//     method: 'POST',
//     body: JSON.stringify({
//       'name': form.name,
//       'city': form.city,
//       'state': form.state,
//       'phone': form.phone,
//       'genres': form.genres,
//       'facebook_link': form.facebook_link
//     }),
//     headers: {
//       'Content-Type': 'application/json'
//     }
//   })
//   .then(response => {response.json()})
//   .then(jsonresponse => {
//     console.log(jsonresponse);
//   })
// }
