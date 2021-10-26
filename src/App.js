import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';


function App() {
	const args = JSON.parse(document.getElementById("data").text);
	const current_user_ids = args.user_artist_ids;
	const [artistList, setartistList] = useState(current_user_ids);
	const textInput = useRef(null);
	//^	<button onClick={deleteArtist(artist)}>Delete</button>
	var update;

	console.log("current user ids:", current_user_ids);
	console.log("artist list:", artistList);

	function addArtist() {
		let artistId = textInput.current.value;
		console.log("text input current val:", artistId);
		setartistList([...artistList, artistId]);
		textInput.current.value = "";
		console.log("add artist artist list:", artistList);
	}

	// function deleteArtist(artistId) {
	// 	console.log(artistId);
	// 	//delete_list.push(artistId);
	// 	console.log(delete_list);
	// 	setartistList(artistList.filter((artist) => artist !== artistId));
	// 	console.log(artistList);
	// }

	function saveArtist() {
		let add_list = artistList.filter(f => !current_user_ids.includes(f));
		let delete_list = current_user_ids.filter(f => !artistList.includes(f));
		console.log("add list: ", add_list);
		console.log("delete list: ", delete_list);

		update = {
			"add": add_list,
			"delete": delete_list
		}
		console.log(JSON.stringify(update));
		fetch('/save', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(update)
		})
			.then(response => response.json())
			.then(data => {
				console.log(data);
				setartistList(data.user_artists_server);
			})
		window.location.reload();
		window.location.reload();

	}

	// const [numClicks, setNumClicks] = useState(0);
	// function onButtonCLick() {
	// 	console.log(JSON.stringify({ "num_clicks": numClicks }));
	// 	fetch('/increment', {
	// 		method: 'POST',
	// 		headers: {
	// 			'Content-Type': 'application/json'
	// 		},
	// 		body: JSON.stringify({ "num_clicks": numClicks }),
	// 	}).then(response => response.json()).then(data => {
	// 		console.log(data);
	// 		setNumClicks(data.num_clicks_server);
	// 	});
	// }
	return (
		<body>
			<div class="topnav">
				<h1>
					<a href="https://github.com/csc4350-f21/project2-nmohamed6"><i class="fab fa-github"></i></a>
				</h1>
				<h1>{args.current_username} music!</h1>
				<h1><a href="/logout">
					<i class="fas fa-sign-out-alt"></i></a>
				</h1>
			</div>
			<main id="main">
				{/* <div>
					<button onClick={onButtonCLick}>Click me</button>
					<p>Button has been clicked {numClicks} times!</p>


				</div> */}

				{args.has_artists_saved ? (
					<div class="row">
						<div class="column">
							<div class="card">
								<h1 id="title">
									Your saved artists
								</h1>
								<ul>  {artistList.map((item) => <li>{item}</li>)}
								</ul>

								<p>Add an artist ID!</p>

								<div>
									<input type="text" ref={textInput} placeholder="Artist ID" required />
									<button onClick={addArtist}> Add artist</button>
								</div>
								<button onClick={saveArtist}>Save!</button>

							</div>

							<div class="card">
								<h1 id="title">
									Artist: {args.name}
								</h1>
								<img id="artistImg" src={args.img} />
							</div>


						</div>

						<div class="column">
							<div class="card">
								<h1 id="title">Now Playing: {args.trackName}</h1> <img src={args.trackImg} />
								<audio controls>
									<source src={args.trackAudio} type="audio/mpeg" /> Audio file not supported for specific track.
									Refresh browser to get new one!
								</audio>
								<p> NOTE: If audio player is not playing, the audio file is not available for this specific track.
									Refresh your browser to get new one!</p>
								<br /> <a href="{args.lyricLink}">Genius Lyrics</a>
							</div>
						</div>
					</div>
				) :
					(<><p> Looks like you haven't added any artists yet. </p>

						<p>Add some artist IDs!</p>

						<ul>  {artistList.map((item) => <li>{item}</li>)}
						</ul>

						<div>
							<input type="text" ref={textInput} placeholder="Artist ID" required />
							<button onClick={addArtist}> Add artist</button>
						</div>
						<button onClick={saveArtist}>Save!</button>
						<p>After saving, refresh your browser to view your page! </p>

					</>)
				}
			</main>
			<div class="footer"> Created by Naima Mohamed
				<br /> Icons by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a
					href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
			</div>

		</body>
	);
}

export default App;
