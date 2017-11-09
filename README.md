Debian/Ubuntu 用 Mailman 2.1 パッケージ + 日本語 UTF-8 対応 + α
======================================================================

  * Copyright (c) 2013-2017 SATOH Fumiyasu @ OSS Technology Corp., Japan
  * License: GNU General Public License version 2
  * URL: <https://github.com/fumiyas/mailman-ja-utf8-debian>
  * Blog: <http://fumiyas.github.io/>
  * Twitter: <https://twitter.com/satoh_fumiyasu>

これは何?
----------------------------------------------------------------------

Debian の Mailman 2.1 パッケージに以下の独自変更・拡張を加えたものです。

  * メールのデコード時にリストの文字エンコードよりメールの文字エンコードを
    優先する。
      * `mailman-2.1.11-prefer-message-encoding.patch`
  * 不正な日本語文字エンコーディングを含むメールの対応。
      * `mailman-2.1.11-no-load-iso2022jp.patch`
      * Python-NKF の nkf_codecs を利用。(要インストール。`pip install nkf`)
      * https://github.com/fumiyas/python-nkf
  * Postfix VERP 対応の強化。
      * `mailman-2.1-postfix-verp.patch`
      * FreeBSD の Postfix port のパッチを移植。
  * コマンドラインによる管理を root 権限でも list 権限でも可能にする調整。
      * `mailman-2.1.11-aliases-mode.patch`
      * Postfix 用の `aliases.db`, `virtual-mailman.db` ファイルのモードを
        `aliases`, `virtual-mailman` ファイルと一致させるパッチ。
        (list グループに書き込み権を追加)
  * 各種通知メッセージを識別しやすいように `Subject` にリスト名を含める。
      * `mailman-2.1.17-add-listname-to-subject-in-notice.patch`
  * エラーメールを自動処理しない設定 (かつ配送エラー自動検出で検出できなかった
    エラーメールをリスト管理者宛に送る設定) のとき、エラーメールを黙って
    捨てずにリスト管理者宛に転送する。
      * `mailman-2.1.17-bounce-to-owner-if-no-processing.patch`
  * 旧式の「リスト名-admin」アドレスの完全廃止。
      * `mailman-2.1-obsolete-admin-address.patch`
      * 「`*-admin`」という名前のリスト名が利用可能になる。
  * 保存書庫の mbox ファイルを月一回ローテート、圧縮する。
      * FIXME: 現状では `arch --wipe` したときに処理対象にならないので注意。

TODO
----------------------------------------------------------------------

  * `arch` をローテートした mbox ファイルに対応。
  * 少し壊れたヘッダー MIME エンコーディング対応
      * [Python-ml-jp 5042] Re: メールの日本語件名を記述通り復元するには？
          * http://www.python.jp/pipermail/python-ml-jp/2010-September/010534.html

参照
----------------------------------------------------------------------

  * Mailman
      * http://www.list.org/
      * https://launchpad.net/mailman
  * Debian Mailman パッケージのリポジトリー
      * http://anonscm.debian.org/viewvc/pkg-mailman/trunk/
      * svn://anonscm.debian.org/pkg-mailman/trunk

メモ
----------------------------------------------------------------------

```console
$ git checkout .
$ QUILT_PATCHES=debian/patches quilt pop -af
$ v=$(sed -n '1{s/^.*(//;s/^[0-9]*://;s/-.*//;p}' debian/changelog)
$ tar \
  -czf ../mailman_$v.orig.tar.gz \
  --owner 0 \
  --group 0 \
  --transform="s|^|mailman-$v/|" \
  $(git ls-files |egrep -v '^(debian|tags|README\.md)$') \
;
```
