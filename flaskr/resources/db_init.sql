CREATE TABLE `securityKey` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `algorithm` varchar(10) COLLATE utf8_bin NOT NULL,
    `publicKey` varchar(2048) NOT NULL,
    `privateKey` varchar(8192) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1;

CREATE TABLE `refreshToken` (
    `token` binary(16) PRIMARY KEY,
    `userId` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;