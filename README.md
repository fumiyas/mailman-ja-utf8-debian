Debian/Ubuntu 用 Mailman 2.1 パッケージ + 日本語 UTF-8 対応 + α
======================================================================

  * Copyright (c) 2013 SATOH Fumiyasu @ OSS Technology Corp., Japan
  * License: GNU General Public License version 2
  * URL: <https://github.com/fumiyas/mailman-ja-utf8-debian>
  * Blog: <http://fumiyas.github.io/>
  * Twitter: <https://twitter.com/satoh_fumiyasu>

これは何?
----------------------------------------------------------------------

Debian の Mailman 2.1 パッケージに以下の独自変更・拡張を加えたものです。

  * 日本語向けの文字エンコーディングを UTF-8 に変更。
    * オリジナルは EUC-JP を利用しており、ユニコード固有文字などを扱えない。
    * 既存の EUC-JP で作成・運用しているリストを移行するには各種の
      文字エンコーディング変換作業が必要です。
  * Postfix VERP 対応の強化。(FreeBSD の Postfix port のパッチを移植)
  * Postfix 用の aliases.db, virtual-mailman.db ファイルのモードを
    aliases, virtual-mailman ファイルと一致させる。
  * 保存書庫の mbox ファイルを月一回ローテート、圧縮する。
  * 不正な日本語文字エンコーディングを含むメールの対応。
    * Python-NKF の nkf_codecs を利用。(別途インストール)
    * https://github.com/fumiyas/python-nkf

