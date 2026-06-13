<!DOCTYPE HTML>
<html lang="ja">
<head>
	<title>監視カメラApp</title>
	<!--5秒ごとに画面更新 -->
	<meta http-equiv="refresh" content="5">
	<style>
		*{outline: 1px solid red; margin:0; box-sizing: border-box;}
		.btn{justify-content:space-between; padding:5px 10px; margin:0 10px;}
		.sensor_val{color:red;}
		td{font-size:90%; width:max-content;}
		td.btncontainer{ display:flex;}
		td.camera-container {
			position: relative; /* 重ね合わせの基準位置にする */
			text-align: center;
			background-color: #f0f0f0;
		}
		.camera-offline-text {
			position: absolute; /* 親枠の中での絶対配置 */
			top: 50%;
			left: 50%;
			transform: translate(-50%, -200%);
			z-index: 1; /* 第1層（底） */
			color: #666;
		}
		img#scamera {
			position: relative;
			z-index: 2; /* 第2層（テキストの上） */
			width: 100%;
			height: 250px;
			object-fit: contain;
		}
	</style>
</head>
<body>
	<table border=1>
	<tr>
		<td colspan=3 width=450 height=250 class="camera-container">
			<span class="camera-offline-text"> ※カメラがOFFになっています</span>
			<img src="http://192.168.11.134:8080/?action=stream" id="scamera" alt="LiveCmaera" width=450 height=250>
		</td>
	</tr>
	<tr>
		<td colspan=2 class="btncontainer">
			<a href="/scamera/on" class="btn btn-on"><button>カメラON</button></a>
			<a href="/scamera/off" class="btn btn-off"><button>カメラOFF</button></a>
		</td>
		<td>
			<a href="/alert/on"><button>Alertボタン</button></a>
		</td>
	</tr>
	<tr>
		<td>気温表示：<span class="sensor_val">{{values["temp"]}}度</span></td>
		<td>湿度表示：<span  class="sensor_val">{{values["humi"]}}％</span></td>
		<td>気圧表示</td>
	</tr>
	<tr>
		<td colspan=2>
		距離センサー判定結果
		</td>
		<td ><a href="/snap/on"><button>SnapShotボタン(ダウンロード用)</button></a>
		<br><small>※カメラONにしてから押してね</small></td>
	</tr>
	</table>
</body>
</html>