Debian/Ubuntu 用 Mailman 2.1 パッケージ + 日本語 UTF-8 対応 + α
======================================================================

  * Copyright (c) 2013-2014 SATOH Fumiyasu @ OSS Technology Corp., Japan
  * License: GNU General Public License version 2
  * URL: <https://github.com/fumiyas/mailman-ja-utf8-debian>
  * Blog: <http://fumiyas.github.io/>
  * Twitter: <https://twitter.com/satoh_fumiyasu>

これは何?
----------------------------------------------------------------------

Debian の Mailman 2.1 パッケージに以下の独自変更・拡張を加えたものです。

  * 日本語向けの文字エンコーディングを UTF-8 に変更。
      * `mailman-2.1.16rc2-ja-utf8.patch`
      * `mailman-2.1.11-prefer-message-encoding.patch`
      * オリジナルは EUC-JP を利用しており、ユニコード固有文字などを扱えない。
      * 既存の EUC-JP で作成・運用しているリストを移行するには各種の
        文字エンコーディング変換作業が必要です。
  * Postfix VERP 対応の強化。
      * `mailman-2.1.16rc2-postfix-verp.patch`
      * FreeBSD の Postfix port のパッチを移植。
  * コマンドラインによる管理を root 権限でも list 権限でも可能にする調整。
      * `mailman-2.1.11-aliases-mode.patch`
      * Postfix 用の `aliases.db`, `virtual-mailman.db` ファイルのモードを
        `aliases`, `virtual-mailman` ファイルと一致させるパッチ。
        (list グループに書き込み権を追加)
      * 保存書庫格納ディレクトリの所有権を list:www-data から www-data:list
        に変更。(リストごとの保存書庫ディレクトリの所有者が root:list または
        list:list になり、list 権限で書き込めるようになる)
  * 保存書庫の mbox ファイルを月一回ローテート、圧縮する。
      * FIXME: 現状では `arch --wipe` したときに処理対象にならないので注意。
  * 各種通知メッセージを識別しやすいように `Subject` にリスト名を含める。
      * `mailman-2.1.17-add-listname-to-subject-in-notice.patch`
  * エラーメールを自動処理しない設定 (かつ配送エラー自動検出で検出できなかった
    エラーメールをリスト管理者宛に送る設定) のとき、エラーメールを黙って
    捨てずにリスト管理者宛に転送する。
      * `mailman-2.1.17-bounce-to-owner-if-no-processing.patch`
  * 配信するメールの `Reply-To`, `List-Id` にリストの説明を含めない。
      * `mailman-2.1-no-description-in-header.patch`
      * 説明に日本語が含まれていると UTF-8 の MIME エンコーディングとなるが、
        ISO-2022-JP なヘッダーで投稿されるとエンコーディングが混在し、
        一部のメーラー (Becky!) が返信時に壊れたヘッダーを作ってしまうため、
        これを回避する。
  * 旧式の「リスト名-admin」アドレスの完全廃止。
      * `mailman-2.1-obsolete-admin-address.patch`
      * 「`*-admin`」という名前のリスト名が利用可能になる。
  * 不正な日本語文字エンコーディングを含むメールの対応。
      * `mailman-2.1.11-no-load-iso2022jp.patch`
      * Python-NKF の nkf_codecs を利用。(要インストール。`pip install nkf`)
      * https://github.com/fumiyas/python-nkf
  * Mailman アップストリームパッチのバックポート
      * `mailman-2.1.17-postfix-virtual-case.patch`

TODO
----------------------------------------------------------------------

  * `arch` をローテートした mbox ファイルに対応。
  * `subject_prefix` のスレッド ID 対応。
      * https://gist.github.com/fumiyas/8272130
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
$ quilt pop -af
$ v=$(sed -n '1{s/^.*(//;s/^[0-9]*://;s/-.*//;p}' debian/changelog)
$ tar -cf - --owner 0 --group 0 `ls -d * \
  |egrep -v '^(debian|tags|README\.md)$'` \
  |tarcust -s "s|^|$v/|" \
  |gzip \
  >../mailman_$v.orig.tar.gz
```

