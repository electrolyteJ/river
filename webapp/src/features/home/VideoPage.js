
import React, { Component } from 'react';
import videojs from 'video.js';
//eslint-disable-next-line
import Hls from 'hls.js';
//eslint-disable-next-line
import Reflv from 'reflv';

export default class VideoPage extends Component {
    constructor(props) {
        super(props);
        this.handleLoadPlaylist = this.handleLoadPlaylist.bind(this);
    }
    handleLoadPlaylist() {
        console.log('handleLoadPlaylist ')
        // this.video.play();
        this.player.play()

    }
    render() {
        return (
            <div className="box">
                <div className="left-box">
                    {/* <Reflv
                        url={'http://127.0.0.1:7001/live/movie.flv'}
                        type="flv"
                        isLive
                        cors
                    /> */}
                    <video id="my-player1">
                    </video >
                    <button type="button" className="btn btn-outline-primary" onClick={this.handleLoadPlaylist}>{"Play"}</button>
                </div>
                <div className="right-box">
                    <video id="my-player" style={{ display: 'none' }} />
                </div>
            </div >
        );
    }
    componentDidMount() {
        var options = {};
        this.player = videojs('my-player', options, function onPlayerReady() {
            videojs.log('Your player is ready!');
            this.on('ended', function () {
                videojs.log('Awww...over so soon?!');
            });
        });
        this.player.src({
            // poster: 'd2zihajmogu5jn.cloudfront.net/bipbop-advanced/bipbop_16x9_variant.png',
            // src: '//d2zihajmogu5jn.cloudfront.net/bipbop-advanced/bipbop_16x9_variant.m3u8',
            // src: '//localhost:8080/playlists/2',
            // src: '//localhost:8081/live/movie.m3u8',
            src: 'http://127.0.0.1:7002/live/movie.m3u8',
            type: 'application/x-mpegURL',
        });
    }
}
