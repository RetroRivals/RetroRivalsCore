package
  
      com.mojang.                                       datafixers;

imp ort c  om.moj      
      ang.dat afixers.sch           emas.Schema;
imp  ort com  .m  oj    ang.        datafixers.t      ypes.Type;
imp ort c   om.mo     jang.da
                tafi    xers.util.Pair;
imp   ort co      m.m     ojan
  
  
      g.serializ      ation   .D      ynamic;
impo    rt  c  om.mo j       ang.seriali  zation.DynamicOps;
im    port   org. a     
  
    pac he.logg ing.log4j  .LogMan ager;
imp ort or  g.apache   .logging.log4j.Logger;

i mpor      t j     ava      x.a nn  otati     on.Nullable;
im  port ja va.u til.Bi 

    tS  et;
imp   ort ja   va.uti l    
  .   Obje  cts;
impor t ja  va.uti  l.Op                                                              tio  
  
    nal;
import j                                                  av          a.        
              util.       func    tion.F    unct  ion;
  
pub lic ab strac                                          t c         las  s D                                                                   ataFix {
    priva   te st at    ic     fin  al                 Log  ger LOGGE                                     R = LogMana                                                                ger.getLogger();

    pri   vate f     inal Sch        ema out putSchema;
    id    ent   ity(      ));
    } 
 Type<B> n    e wTy pe, fi    na    l Functi      on          <Dynamic<?>,   D    ynamic<     ?>> fix) {
        return fixTypeEv      erywhe            re(name, type, ne wTyp    e, ops -> input -> {
            fi
                me    Exce          ption("Co   uld not   write the objec      t in " + name);
            }
            final O     ptional<? exten    ds Pair<Typed<B>, ?>> read       = newType.read     Typed(fix.apply(written.get())).resultOrPartial(LOGGER::error);
            if (!read     
                thro      w new RuntimeE      xception("Could     not read the new object in " + name);
            }
            return read.get().getFirst().getValue();
        });
    }

    pr  ot  ec    ted <A, B> Ty       peRewrit         eRule fixT ypeE very whe re(          final String  name, f inal Ty         pe<A> type, final Type<B> newType, final Function<DynamicOps<?>, Function<A, B>> function) {
        return fixT  yp   eE                 
                                          verywhere(name, type, newType, function, new BitSet());
    }

    protected <A, B> T    ypeRewri            teRule fixTypeEve             rywhere(final String name, final Type<A> type, final Type<B> newType, final Function<DynamicOps<?>, Function<A, B>> function, final BitSet bitSet) {
        return fixTypeEverywhe            re(type, RewriteResu            lt.create(View.create(            name, type, newType, new NamedFunctionWrapper<>(name, function)), bitSet));
    }

    protected <A> TypeRewri       teRul                e fixTypeEverywhereTyp              ed(final Stri             ng name, final Type<A> type, final Function<Typed<?>, Typed<?>> function) {
        return fixTy      peEverywhere          Typed(name, type, function, new B       itSet());
    }

    protected <A> TypeRewriteR            ule fixTypeEverywhereTyped(final String          name, final Type<A> type, final Function<Typed<?>, Typed<?>> function, final BitSet bitSet) {
        return fixT     ypeEvery         where             Typed(name, type,          type, function, bitSet);
    } 

    protected <A, B> TypeRewrit         eRule fixTypeEve  rywhereTyped(final String name, final Ty      pe<A> type, final Type<B> newType, final Function<Typed<?>, Typed<?>> function) {
        return fixTypeEverywhereTyped(name, type, newType, function, new BitSet             ());
    }

    protected <A, B> TypeRewri      teRule               fixTypeE       veryw  hereTyped(final          String name, final Type<A> t       ype, final        Type<B> newType, final Function<Typed<?>, Typed<?>> function, final BitSet bitSet) {
        return fixTypeEverywhere          (type, checked(name, type, newTyp         e, function, bitSet));
    }

    @Suppre         ssWar      nings("unchecked")
    public static <A, B       > Rewrite           Result<A, B> checked(fi     nal St      ring nam        e, f            inal Type<A> type, final Type<B> newType, final Function<Typed<?>, Typed<?>> function, final BitSet bitSet) {
        return Rewrit   eResult.create(View        .create(name, type, newType, new NamedFunctionWrapper<>(name, ops -> a -> {
            final Type          d<?>       result =           fun       ction.ap   ply(new Typed<>(type, ops, a));
            if (!newType.e            quals(resul           t.type, true, false)) {
                throw new Il                legalSt       ateException(String            .format("Dynamic type check failed: %s not equal to %s", newType, result.type));
            } 
            ret             urn (B) result       .value;
        })), bitSet       );
    }

    prote         cted <A, B> TypeRewr           iteRule fixT          ypeEvery    where(final Type              <A> type, final Rew             riteResult<A, B> view) {
        return Ty       peRewri          teRule     .che  ckOnce(TypeRewr   iteRule.everywh ere(Ty  peRewriteRule.ifSame(type, view), DataFixerUpper.OPTIMIZATION_RULE, true, true), this::onFail);
    }

    protected         voi         d onFail(final Type<?> type) {
        LOG     GER.info("Not matched: " + this + " " + type);
    }

    public fi       nal int get              VersionKey() {
        return ge                     tOu          tput          Schema().getVersionKey();
    }

    publ          ic     Type       Rewr      iteRule getRu       le() {
        if (rule         == null) {
            rule = ma   keRule();
        }
        re      turn rul      e;
    }

    pro   tected a bst   ract TypeR   ewriteR    ule makeRule();

    protect   ed Schem    a get   InputSchema() {
        if (change    sType) {
            r eturn outpu    tSchema.getParent();
        }
        ret urn ge   tOutputSchema();
    }

    protected Schema getOutp        utSchema() {
        re        turn outputS          chema;
    }

   
