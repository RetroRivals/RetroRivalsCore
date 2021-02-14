package
  
      com.mojang.datafixers;

import com.moj      
      ang.datafixers.schemas.Schema;
import com.mojang.datafixers.types.Type;
import com.mojang.da
                tafixers.util.Pair;
import com.mojan
  
  
      g.serialization.Dynamic;
import com.mojang.serialization.DynamicOps;
import org.a    
  
    pache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.annotation.Nullable;
import java.util.Bi 

    tSet;
import java.util    
  .Objects;
import java.util.Optio  
  
    nal;
import java.        
              util.function.Function;

public abstract class DataFix {
    private static final                 Logger LOGGER = LogManager.getLogger();

    private final Schema outputSchema;
    privat            e final boolean changesType;
   lable
    private TypeRewriteRule rule;

    public DataFix(final Schema outputSchema, final boolean changesType) {
        this.ou   
          tputSchema = outputSchema;
        thi 
      
            s.changesType = changesType;
    }

    protected <A> TypeRewriteRu           
  
                                le fixTypeEverywhere(final String name, final Type<A> type, final Function<DynamicOps<?>, Function<A, A>> function) {
        return fixTypeEverywhere(name, type, type, function, new BitSet());
    }

    @SuppressWarnin

    protected TypeRewriteRule writeAndRead(final String name, final Type<?> type, final Type<?> newType) {
        return writeFixAndRead(name, ty 
                                pe, newType, Function.identity());
    }

    protected <A, B> TypeRewriteRul           e writeFixAndRead(final String name, final T  ype<A> type, final Type<B> newType, final Function<Dynamic<?>, Dynamic<?>> fix) {
        return fixTypeEverywhe            re(name, type, newType, ops -> input -> {
            final Opti          on                    
              al<? extends Dynamic<?>> written = type.writeDynamic(ops, input).resultOrPartial(LOGGER::error);
            if (!w                    ritten.isPresent()) {
                throw new Runti             
                meException("Could not write the object in " + name);
            }
            final Optional<? extends Pair<Typed<B>, ?>> read = newType.readTyped(fix.apply(written.get())).resultOrPartial(LOGGER::error);
            if (!read     
                throw new RuntimeException("Could not read the new object in " + name);
            }
            return read.get().getFirst().getValue();
        });
    }

    protected <A, B> TypeRewrit         eRule fixT ypeE very whe re(          final String  name, f inal Ty         pe<A> type, final Type<B> newType, final Function<DynamicOps<?>, Function<A, B>> function) {
        return fixT  ypeE                 
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

    protected <A, B> TypeRewrit         eRule fixTypeEverywhereTyped(final String name, final Ty      pe<A> type, final Type<B> newType, final Function<Typed<?>, Typed<?>> function) {
        return fixTypeEverywhereTyped(name, type, newType, function, new BitSet             ());
    }

    protected <A, B> TypeRewri      teRule               fixTypeEverywhereTyped(final          String name, final Type<A> t       ype, final        Type<B> newType, final Function<Typed<?>, Typed<?>> function, final BitSet bitSet) {
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

    protected Schema getOutputSchema() {
        return outputSchema;
    }

    private static final class NamedFunctionWrapper<A, B> implements Function<DynamicOps<?>, Function<A, B>> {
        private final String name;
        private final Function<DynamicOps<?>, Function<A, B>> delegate;

        public NamedFunctionWrapper(final String name, final Function<DynamicOps<?>, Function<A, B>> delegate) {
            this.name = name;
            this.delegate = delegate;
        }

        @Override
        public Function<A, B> apply(final DynamicOps<?> ops) {
            return delegate.apply(ops);
        }

        @Override
        public boolean equals(final Object o) {
            if (this == o) {
                return true;
            }
            if (o == null || getClass() != o.getClass()) {
                return false;
            }
            final NamedFunctionWrapper<?, ?> that = (NamedFunctionWrapper<?, ?>) o;
            return Objects.equals(name, that.name);
        }

        @Override
        public int hashCode() {
            return Objects.hash(name);
        }
    }
}
