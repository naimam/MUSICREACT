import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';


function App() {
	const args = JSON.parse(document.getElementById("data").text);
	let artist_len = false;
	return (
		<>
			<div class="topnav">
				<h1>
					<a href="https://github.com/csc4350-f21/project2-nmohamed6"><i class="fab fa-github"></i></a>
				</h1>
				<h1>current_user.username var's music!</h1>
				<h1><a href="{{ url_for('logout')}}">
					<i class="fas fa-sign-out-alt"></i></a>
				</h1>
			</div>
			<main id="main">
				<div>
					<p>Add an artist ID!</p>
					<form method="POST">
						<input type="text" name="artistId" placeholder="Artist ID" required />
						<input type="submit" value="Submit!" />
					</form>
				</div>

				{artist_len ? (
					<div class="row">
						<div class="column">
							<div class="card">
								<h1 id="title">
									Artist: namevar
								</h1>
								<img id="artistImg" src="{{img}}" />
							</div>

							<div class="card">
								<p> user's saved artists here</p>
							</div>
						</div>

						<div class="column">
							<div class="card">
								<h1 id="title">Now Playing: trackNameVar</h1> <img src="{{trackImg}}" />
								<audio controls>
									<source src="{trackAudiovar.mp3" type="audio/mpeg" /> Audio file not supported for specific track.
									Refresh browser to get new one!
								</audio>
								<p> NOTE: If audio player is not playing, the audio file is not available for this specific track.
									Refresh your browser to get new one!</p>
								<br /> <a href="/lyricLinkVar">Genius Lyrics</a>
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

		</>
	);
}

export default App;
