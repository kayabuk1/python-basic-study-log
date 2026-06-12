<!DOCTYPE HTML>
<html lang="ja">
<head>
	<title>監視カメラApp</title>
	<!--5秒ごとに画面更新 -->
	<meta http-equiv="refresh" content="5">
	<style>
		*{outline: 1px solid red;}
		img#scamera{width: 100%;}
	</style>
</head>
<body>
	<table border=1>
	<tr>
		<td colspan=3 width=450 height=250>
			<img src="http://192.168.11.134:8080/?action=stream" id="scamera" alt="LiveCmaera">
				<a href="/scamera/on" class="btn btn-on">カメラON</a>
				<a href="/scamera/off" class="btn btn-off">カメラOFF</a>
			Snap Shot ボタン（ダウンロード用）
		</td>
	</tr>
	<tr>
		<td colspan=2>
		Camera ON ボタン
		Camera OFF ボタン
		</td>
		<td>
			Alert ボタン
		</td>
	</tr>
	<tr>
		<td>気温表示</td>
		<td>湿度表示</td>
		<td>気圧表示</td>
	</tr>
	<tr>
		<td colspan=3>
		距離センサー判定結果
		</td>
	</tr>
	</table>
</body>
</html>