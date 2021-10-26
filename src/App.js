import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';


function App() {
	const args = JSON.parse(document.getElementById("data").text);
	const user_saved_artists = args.user_artist_ids.map((artist) =>
		<li>{artist}</li>
	);

	const [numClicks, setNumClicks] = useState(0);
	function onButtonCLick() {
		console.log(JSON.stringify({ "num_clicks": numClicks }));
		fetch('/increment', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ "num_clicks": numClicks }),
		}).then(response => response.json()).then(data => {
			console.log(data);
			setNumClicks(data.num_clicks_server);
		});
	}
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
				<div>
					<p>Add an artist ID!</p>
					<button onClick={onButtonCLick}>Click me</button>
					<p>Button has been clicked {numClicks} times!</p>


					<form method="POST">
						<input type="text" name="artistId" placeholder="Artist ID" required />
						<input type="submit" value="Submit!" />
					</form>
				</div>

				{args.has_artists_saved ? (
					<div class="row">
						<div class="column">
							<div class="card">
								<h1 id="title">
									Your saved artists
								</h1>
								<ul>{user_saved_artists}</ul>
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
					(<p> Looks like you haven't added any artists yet... </p>)
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
