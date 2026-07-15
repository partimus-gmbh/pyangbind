"""Differential test corpus, batch 5: former known-divergence fixes."""
from cases import M


CASES = [
    dict(
        name="leafref-instance-scope",
        yang=M("dt-lscope", """
  list box {
    key "name";
    leaf name { type string; }
    list srv { key "sn"; leaf sn { type string; } }
    leaf pick { type leafref { path "../srv/sn"; } }
    leaf-list picks { type leafref { path "../srv/sn"; } }
  }
"""),
        docs=[
            ("same-entry-ok", {"dt-lscope:box": [
                {"name": "b1", "srv": [{"sn": "s1"}], "pick": "s1"}]}),
            ("cross-entry-dangling", {"dt-lscope:box": [
                {"name": "b1", "srv": [{"sn": "only-b1"}]},
                {"name": "b2", "pick": "only-b1"}]}),
            ("leaflist-cross-entry", {"dt-lscope:box": [
                {"name": "b1", "srv": [{"sn": "only-b1"}]},
                {"name": "b2", "srv": [{"sn": "own"}], "picks": ["own", "only-b1"]}]}),
        ],
    ),
    dict(
        name="unique-descendant",
        yang=M("dt-uniqd", """
  list l {
    key "k";
    unique "c/v name";
    leaf k { type string; }
    leaf name { type string; }
    container c { leaf v { type uint8; } }
  }
"""),
        docs=[
            ("dup-pair", {"dt-uniqd:l": [
                {"k": "a", "name": "n", "c": {"v": 1}},
                {"k": "b", "name": "n", "c": {"v": 1}}]}),
            ("distinct-descendant", {"dt-uniqd:l": [
                {"k": "a", "name": "n", "c": {"v": 1}},
                {"k": "b", "name": "n", "c": {"v": 2}}]}),
            ("absent-leaf-skips", {"dt-uniqd:l": [
                {"k": "a", "name": "n"},
                {"k": "b", "name": "n", "c": {"v": 1}}]}),
        ],
    ),
    dict(
        name="derived-from-transitive",
        yang=M("dt-dft", """
  identity base;
  identity mid { base base; }
  identity deep { base mid; }
  identity other { base base; }
  leaf kind { type identityref { base base; } }
  leaf need-mid { type string; must "derived-from(../kind, 'mid')"; }
  leaf need-mid-self { type string; must "derived-from-or-self(../kind, 'mid')"; }
"""),
        docs=[
            ("transitive-true", {"dt-dft:kind": "deep", "dt-dft:need-mid": "x"}),
            ("self-not-derived", {"dt-dft:kind": "mid", "dt-dft:need-mid": "x"}),
            ("unrelated", {"dt-dft:kind": "other", "dt-dft:need-mid": "x"}),
            ("or-self-true", {"dt-dft:kind": "mid", "dt-dft:need-mid-self": "x"}),
            ("or-self-transitive", {"dt-dft:kind": "deep", "dt-dft:need-mid-self": "x"}),
            ("or-self-unrelated", {"dt-dft:kind": "other", "dt-dft:need-mid-self": "x"}),
        ],
    ),
]
