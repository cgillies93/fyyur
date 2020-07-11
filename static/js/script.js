window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

const modal = document.getElementById("myModal");
const span = document.getElementsByClassName("close")[0];
const cancelDelete = document.getElementsByClassName("cancel-delete-btn")[0];
const deleteVenueBtn = document.getElementById("deleteVenueBtn");
const deleteArtistBtn = document.getElementById("deleteArtistBtn");
const confirmVenueDelete = document.getElementsByClassName("confirm-venue-delete-btn")[0];
const confirmArtistDelete = document.getElementsByClassName("confirm-artist-delete-btn")[0];
const seeking = document.getElementsByClassName("seeking_check")[0];
const seekingDescription = document.getElementsByClassName("seeking_description")[0];
const seekingLabel = document.getElementsByClassName("seeking_label")[0];


////MODAL BUTTONS
if (span != null) {
  span.onclick = () => {
    modal.style.display = "none";
  }
}

if (cancelDelete != null) {
  cancelDelete.onclick = () => {
    modal.style.display = "none";
  }
}

////GET VENUE ID FOR DELETE
let v_id = document.getElementById("venue_id");
let v_id_text = '';
if (v_id != null) {
  v_id_text = v_id.innerText;
}
const venue_id = v_id_text.split(" ")[1];

////GET ARTIST ID FOR DELETE
let a_id = document.getElementById("artist_id");
let a_id_text = '';
if (a_id != null) {
  a_id_text = a_id.innerText;
}
const artist_id = a_id_text.split(" ")[1];


////DELETE VENUE BUTTONS
if (deleteVenueBtn != null){
  deleteVenueBtn.onclick = () => {
    modal.style.display = "block";
  }
}

if (confirmVenueDelete != null) {
  confirmVenueDelete.onclick = (e) => {
    e.preventDefault();

    fetch(`${venue_id}`, {
      method: 'DELETE'
    })
    .then(response => {window.location = "/"})
  }
}


////DELETE ARTIST BUTTONS
if (deleteArtistBtn != null){
  deleteArtistBtn.onclick = () => {
    modal.style.display = "block";
  }
}

if (confirmArtistDelete != null) {
  confirmArtistDelete.onclick = (e) => {
    e.preventDefault();

    fetch(`/artists/${artist_id}`, {
      method: 'DELETE',
      body: {}
    })
    .then(response => {
      window.location = "/";
      console.log(response);
    })
  }
}



////Seeking Toggle
if (seeking != null){
  if (seeking.checked) {
    seekingDescription.style.display = "block";
    seekingLabel.style.display = "block";
  }
  seeking.onclick = () => {
    console.log('click');
    if (seeking.checked) {
      seekingDescription.style.display = "block";
      seekingLabel.style.display = "block";
    }
    else {
      seekingDescription.style.display = "none";
      seekingLabel.style.display = "none";

    }
  }
}





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
